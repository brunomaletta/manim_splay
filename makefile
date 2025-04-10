all:
	manim -p -q m main.py DefaultTemplate 2> /dev/null
h:
	manim -p -q h main.py DefaultTemplate 2> /dev/null

clean:
	rm -rf media
