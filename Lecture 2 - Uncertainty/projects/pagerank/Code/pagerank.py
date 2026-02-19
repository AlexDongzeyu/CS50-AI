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

    prob_dist = {}
    num_pages = len(corpus)
    links = corpus[page]

    # Handling Sink Nodes (Dead Ends)
    # If a page has no outgoing links, we will interpret this as having implicit links to all pages (including itself).
    # This avoids the algorithm getting stuck
    
    if len(links) == 0:
        for p in corpus:
            prob_dist[p] = 1/num_pages
        return prob_dist
    
    # Damping Formula
    # Teleportation (1-d), the user types a random URL
    # We divide this probability evenly across all N pages

    random_prob = (1- damping_factor) / num_pages

    # Surfing (d), the user clicks a link on the current page
    # This probability is split evenly among the specific outgoing links.
    link_prob = damping_factor / len(links)

    for p in corpus:
        # every page receives the base teleportation probability
        prob_dist[p] = random_prob

        # if page p is a valid link from the current page, add surfing probability
        if p in links:
            prob_dist[p] += link_prob

    return prob_dist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize a visit counter for every page in the corpus
    counts = {}
    for page in corpus:
        counts[page] = 0
    
    # The surfer starts at a completely random page (initialization)
    current_page = random.choice(list(corpus.keys()))
    counts[current_page] += 1

    # loop n-1 times
    for _ in range(n - 1):
        # get probability distribution for the next step
        dist = transition_model(corpus, current_page, damping_factor)
        
        # get the pages (states) and their calculated probabilities (weights)
        pages = list(dist.keys())
        weights = list(dist.values())
        
        # determine the next page using weighted random selection
        current_page = random.choices(pages, weights=weights, k=1)[0]
        counts[current_page] += 1

    # normalize counts to create a probability distribution (sum = 1)
    pagerank = {}
    for page, count in counts.items():
        pagerank[page] = count / n
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    threshold = 0.001
    
    # give every page an equal starting rank (1/N where N is number of pages)
    ranks = {}
    for page in corpus:
        ranks[page] = 1 / num_pages
    
    # keep updating ranks until they stabilize (stop changing significantly)
    while True:
        new_ranks = {}
        max_diff = 0
        
        # calculate the new rank for each page in the corpus
        for page in corpus:
            current_rank_sum = 0
            
            # check every other page to see if it links to our current page
            for potential_linker in corpus:
                links = corpus[potential_linker]
                
                # if the potential linker has links and links to our page, 
                # add its rank divided by the number of links it has
                if page in links:
                    current_rank_sum += ranks[potential_linker] / len(links)
                
                # if the potential linker has NO links (dead end),
                # we treat it as linking to all pages equally, so add its rank divided by N
                elif len(links) == 0:
                    current_rank_sum += ranks[potential_linker] / num_pages
            
            # apply the PageRank formula: 
            # new rank = (1-d)/N + d * (sum of contributions from linking pages)
            new_val = ((1 - damping_factor) / num_pages) + (damping_factor * current_rank_sum)
            new_ranks[page] = new_val
            
            # keep track of the biggest change to see if we've converged
            if abs(new_val - ranks[page]) > max_diff:
                max_diff = abs(new_val - ranks[page])
        
        # update all ranks for the next iteration
        ranks = new_ranks
        
        # if the biggest change is smaller than our threshold, we've converged!
        if max_diff < threshold:
            break
            
    return ranks


if __name__ == "__main__":
    main()
