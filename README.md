# How Far Am I?

Have you ever played the game where you navigate from one Wikipedia page to another using the fewest links possible? This project implements exactly that.

[Instagram video demonstrating the game](https://www.instagram.com/reel/C9OXJCCO8mh/?utm_source=ig_web_copy_link)

## How Does It Work?

This project uses a breadth-first search algorithm without relying on graph structures. Instead, it employs a dictionary with lists as the primary data structures. This allows for efficient pathfinding between links with O(1) time complexity for checking if a link has been visited.

### Steps:
1. **Validation**: The algorithm first checks if both the starting and target Wikipedia links are valid.
2. **Scraping**: If the links are valid, the algorithm scrapes the starting Wikipedia page, extracting all the links within `<p>` tags that aren't buttons or part of excluded categories (e.g., archives, help pages).
3. **Building Paths**: The links are added to the dictionary and list, after proving they haven't been visited yet.
4. **Parallel Processing**: The process utilizes multiprocessing to improve speed through parallelization.
5. **Path Reconstruction**: Once the target link is found, the loop ends, and the shortest path (in terms of the number of links) from the starting link to the target one is reconstructed.

## Requirements

- `pip install lxml`
- `pip install fastapi`

## How to Run

1. Run the FastAPI application:
   ```sh
   fastapi run reacher_api.py
   ```
2. Open the `howFarAmI.html` file in your browser and start playing.

## Disclaimer

1. The links must be from Wikipedia in spanish! WIP for a english version
2. This process can take some time depending on the number of pages between the starting and target links.

## Work to Do

- Implement a search for the same link as the starting one.
- Add a stop button.
- Improve the HTML/CSS styling.
- Enhance the README with lessons learned, next steps, and decisions made during the project.