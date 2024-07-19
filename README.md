# How Far Am I?

Have you ever played the game where you navigate from one Wikipedia page to another using the fewest links possible? This does exactly that.

[Instagram video demonstrating the game](https://www.instagram.com/reel/C9OXJCCO8mh/?utm_source=ig_web_copy_link)

## How Does It Work?

This project uses a breadth-first search algorithm without relying on graph structures. Instead, it employs a dictionary and a list, as the primary data structures. This allows for efficient pathfinding between links with O(1) time complexity for checking if a link has been visited, while also being capable of reconstruct the path after reaching the target link.

### Steps:
1. **Validation**: The algorithm first checks if both the starting and target Wikipedia links are valid.
2. **Scraping**: If the links are valid, the algorithm scrapes the starting Wikipedia page, extracting all the links, within `<p>` tags in the body, that aren't buttons or part of excluded categories (e.g., archives, help pages).
3. **Building Paths**: The links are added to the dictionary (key: found link, value: the link of where it was scraped from) and list, after proving they haven't been visited yet.
4. **Parallel Processing**: The process utilizes multiprocessing to improve speed through parallelization.
5. **Path Reconstruction**: Once the target link is found, the loop ends, and the shortest path (in terms of the number of links) from the starting link to the target one is reconstructed.

## How to Run

1. Run the FastAPI application with Poetry
2. Open the `howFarAmI.html` file in your browser and start playing.

### OR

You can test it [here](https://manuelm512.github.io/HowFarAmI/)

## Disclaimer

1. The links must be from Wikipedia in spanish! WIP for an english version.
   Be careful with the accents! If your pasted link has accents, it won't work. Sorry! 
   You need to copy it without accents, probably the best way is to do right-click over the link you want and then the option that says something along the lines of "copy the link...". 
2. This process can take some time depending on the number of pages between the starting and target links.
   To make not-so-long tests, it's advised to choice a target link that you had got surfing between links from the starting one. Two or three pages between one and the other sounds like a nice try!

## Decisions made

**Q.** Why a dictionary?<br>
**A.** It provided me with the capability of asking if the link was already visited in O(1), while also being a not-so-traditinal way of implementing a kind of BFS, so it seemed fun. 
I thought of it as a challenge, and in a way, like the implementation of heap-sort in a list, instead of a tree.

**Q.** Is it really necessary a list?<br>
**A.** I really tried not to use it, however, it was a must in the end. Even if the dictionary already has a list of its keys, when I tried to retrieve them and get one by index, I couldn't find a way of doing so without the use of a cast of dict.keys() to list, which has a time complexity of O(n) (being n the amount of links), resulting in an even more slow algorithm. 

**Q.** Trade off between memory and time complexity? <br>
**A.** Yes, it was something to take into account. Slicing of strings, or trying to only save the non-repeated parts of them, was used in the beginning, however, as I was trying to improve the time needed to run, it was discarded, as the use of slicing had a O(k), being k the amount of characters sliced, and this being done for each link, wasn't really what I was looking for.

## What I learned

1. **Breadth-First Search (BFS) Implementation**:
   - Implemented BFS in a non-traditional way, always aiming for efficiency in terms of time complexity.

2. **Web Scraping Techniques**:
   - How to extract the needed part of the page, excluding the ruled out ones.

3. **Parallel Processing**:
   - Learnt to use multiprocessing, while also how to implement it for this specific case.

4. **Dependency Management with Poetry**:
   - Managed project dependencies using Poetry, simplifying the setup and deployment.

5. **Now with more experience in Python**:
   - Researched plenty of functions time complexities and the best ways to use them.

6. **Deployment and UI Integration**:
   - Deployed a FastAPI application (harder than what I thought it would be) and integrated it with a front-end interface.

## Next steps

Some ideas I had while in the making proccess of this project (that lasted more or less a week).

- Every x amount of links requested, save them and theirs connections, in order to not have so much data in the active memory, and only get back to them when needed to reconstruct the path.
- Caching the data, or storing it in a DB, to reduce the amount of requests, reusing the ones already done between different searchs. 
- Some searchs can be very long, thinking of a way to stop and continue would be nice.
- A toggle button for english to make searching in english wikipedia doesn't sound difficult.

## Work to Do

- Improve style / front-end
- Improve the input of links, not to have problems with accents
