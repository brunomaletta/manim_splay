from manim import *

class DefaultTemplate(MovingCameraScene):
	def construct(self):

		plane = NumberPlane()
		self.add(plane)

		arrow1 = Arrow(buff=0, start=ORIGIN, end=ORIGIN+0.1*RIGHT)
		arrow1.scale(10, about_point=ORIGIN, scale_tips=True)
		arrow1.shift(DOWN)
		arrow2 = Arrow(buff=0, start=ORIGIN, end=ORIGIN+RIGHT)

		self.add(arrow1)
		self.add(arrow2)
