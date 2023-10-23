import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_pages = len(corpus)
    if not corpus[page]:
        # If the current page has no outgoing links, choose randomly among all pages
        return {p: 1.0 / num_pages for p in corpus}

    transition_probabilities = {}
    linked_pages = corpus[page]
    for p in corpus:
        # Probability to transition to linked pages with damping_factor
        if p in linked_pages:
            transition_probabilities[p] = (damping_factor / len(linked_pages))
        else:
            transition_probabilities[p] = 0.0

        # Probability to choose any page with (1 - damping_factor)
        transition_probabilities[p] += (1 - damping_factor) / num_pages

    return transition_probabilities



def sample_pagerank(corpus, damping_factor, n):
    # Initialize PageRank dictionary with all pages and set initial values to 0
    pagerank = {page: 0 for page in corpus}

    # Randomly choose the first sample
    current_sample = random.choice(list(corpus.keys()))

    for _ in range(n - 1):  # -1 because the first sample has already been chosen
        # Increase the PageRank for the current sample by 1
        pagerank[current_sample] += 1

        # Use the transition model to select the next page
        model = transition_model(corpus, current_sample, damping_factor)
        next_sample = random.choices(list(model.keys()), weights=list(model.values()))[0]

        # Update the current sample for the next iteration
        current_sample = next_sample

    # The last sample (n-th) is not incremented in the loop, so we do it here
    pagerank[current_sample] += 1

    # Normalize the PageRank values
    total_samples = n
    pagerank = {page: rank / total_samples for page, rank in pagerank.items()}

    return pagerank





def iterate_pagerank(corpus, damping_factor):
    # Initialize the PageRank values
    num_pages = len(corpus)
    initial_rank = 1.0 / num_pages
    pageranks = {page: initial_rank for page in corpus}

    while True:
        new_pageranks = {}
        diff = 0  # Initialize diff outside the loop

        for page in corpus:
            new_pagerank = (1 - damping_factor) / num_pages

            for linking_page, linked_pages in corpus.items():
                if page in linked_pages:
                    new_pagerank += damping_factor * (pageranks[linking_page] / len(linked_pages))

            new_pageranks[page] = new_pagerank
            diff = max(diff, abs(new_pagerank - pageranks[page]))  # Update diff

        pageranks = new_pageranks

        # Check if no PageRank value changes by more than 0.001
        if diff < 0.001:
            break

    # Normalize the final PageRank values
    total_rank = sum(pageranks.values())
    pageranks = {page: rank / total_rank for page, rank in pageranks.items()}

    return pageranks



if __name__ == "__main__":
    main()
