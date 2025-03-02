## Pygame

[manual](https://www.pygame.org/docs/ref/time.html#pygame.time.get_ticks)

```
source venv/bin/activate
python ball.py
```
## Manim Community 

[docker](https://hub.docker.com/r/manimcommunity/manim)

### To render the scene in a video

```
docker run --rm -it  --user="$(id -u):$(id -g)" -v "$(pwd)":/manim manimcommunity/manim manim test_scenes.py CircleToSquare -qm
```
