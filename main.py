from manim import *
import random

class Node:
	def __init__(self, val, pos, scale):
		self.p = None
		self.l = None
		self.r = None
		self.sz = 1
		self.val = val
		self.pos = pos
		self.scale = scale
		self.circ = None
		self.l_arrow = None
		self.r_arrow = None

class SplayTree:
	def __init__(self, pos, scale):
		self.root = None
		self.pos = pos
		self.scale = scale

class DefaultTemplate(MovingCameraScene):
	REC_SCALE=0.5

	def get_arrow(self, beg, end, node):
		arrow = Arrow(buff=0, start=beg, end=end, stroke_width=5)
		return arrow

	def print_node(self, node, scale):

		circle = Circle(radius=1*scale,stroke_width=0,color=RED, fill_opacity=0.8)
		circle.move_to(node.pos)

		node_text = Text(str(node.val)).scale(1.5*scale)
		node_text.move_to(circle.get_center())
		node_text.add_updater(lambda x: x.move_to(circle.get_center()))

		node.circ = VGroup(circle, node_text)
		self.play(Create(node.circ))

	def get_left_pos(self, node):
			shift = 0.7 * node.scale * (LEFT + DOWN)
			return node.pos + 2.5*shift

	def get_right_pos(self, node):
			shift = 0.7 * node.scale * (RIGHT + DOWN)
			return node.pos + 2.5*shift

	def node_subtree_group(self, node):
		if node is None:
			return VGroup()
		group = VGroup(node.circ)
		if node.l is not None:
			group += self.node_subtree_group(node.l)
		if node.r is not None:
			group += self.node_subtree_group(node.r)
		return group

	def arrow_subtree_vec(self, node):
		if node is None:
			return []
		group = []
		if node.l is not None:
			group.append(node.l_arrow)
			group += self.arrow_subtree_vec(node.l)
		if node.r is not None:
			group.append(node.r_arrow)
			group += self.arrow_subtree_vec(node.r)
		return group

	def update_subtree_pos_and_scale(self, node, pos, scale):
		node.pos = pos
		node.scale *= scale

		if node.l is not None:
			self.update_subtree_pos_and_scale(node.l, self.get_left_pos(node), scale)
		if node.r is not None:
			self.update_subtree_pos_and_scale(node.r, self.get_right_pos(node), scale)

	def focus_on_node(self, splay, cur_scale, node):
		self.play(self.camera.frame.animate
			.scale(node.scale / cur_scale)
			.move_to(node.pos - splay.pos*node.scale / self.REC_SCALE)
			)

	def rotate(self, node):
		p = node.p
		pp = p.p

		if pp is not None:
			p_left = True if pp.l == p else False
			if p_left:
				pp.l = node
			else:
				pp.r = node

		left = True if p.l == node else False
		if left:

			mid = node.r
			p.l = None
			node.r = None

			sub_p = self.node_subtree_group(p)
			sub_p_ar = VGroup(*self.arrow_subtree_vec(p))
			sub_node = self.node_subtree_group(node)
			sub_node_ar = VGroup(*self.arrow_subtree_vec(node))
			sub_mid = self.node_subtree_group(mid) + VGroup(*self.arrow_subtree_vec(mid))

			p_shift = self.get_right_pos(p) - p.pos
			p_scale = self.REC_SCALE

			node_shift = p.pos - node.pos
			node_scale = 1/self.REC_SCALE

			self.update_subtree_pos_and_scale(node, p.pos, node_scale)
			self.update_subtree_pos_and_scale(p, self.get_right_pos(p), p_scale)

			arrow_shift = 0.7 * node.scale * (RIGHT + DOWN)
			new_arrow = self.get_arrow(node.pos+arrow_shift, p.pos-0.5*arrow_shift, node.scale)
			arrow_shift_mid = 0.7 * p.scale * (LEFT + DOWN)

			new_sub_p_ar = VGroup(*[ar.copy().shift(p_shift)
				.scale(p_scale, scale_tips=True, about_point=p.pos)
					for ar in self.arrow_subtree_vec(p)])
			new_sub_node_ar = VGroup(*[ar.copy().shift(node_shift)
				.scale(node_scale, scale_tips=True, about_point=node.pos)
					for ar in self.arrow_subtree_vec(node)])

			if mid is None:
				self.play(
					sub_p.animate.shift(p_shift).scale(p_scale, about_point=p.pos),
					Transform(sub_p_ar, new_sub_p_ar),
					sub_node.animate.shift(node_shift).scale(node_scale,
						about_point=node.pos),
					Transform(sub_node_ar, new_sub_node_ar),
					Transform(p.l_arrow, new_arrow)
				)
			else:
				mid_shift = self.get_left_pos(p) - mid.pos

				self.update_subtree_pos_and_scale(mid, self.get_left_pos(p), 1)

				new_arrow_mid = self.get_arrow(p.pos+arrow_shift_mid,
					mid.pos-0.5*arrow_shift_mid, p.scale)

				self.play(
					sub_p.animate.shift(p_shift).scale(p_scale, about_point=p.pos),
					Transform(sub_p_ar, new_sub_p_ar),
					sub_node.animate.shift(node_shift).scale(node_scale,
						about_point=node.pos),
					Transform(sub_node_ar, new_sub_node_ar),
					Transform(p.l_arrow, new_arrow),
					sub_mid.animate.shift(mid_shift),
					Transform(node.r_arrow, new_arrow_mid)
				)

			node.r_arrow, p.l_arrow = p.l_arrow, node.r_arrow
			p.l = mid
			node.r = p

			if p.l is not None:
				p.l.p = p

		else:

			mid = node.l
			p.r = None
			node.l = None

			sub_p = self.node_subtree_group(p)
			sub_p_ar = VGroup(*self.arrow_subtree_vec(p))
			sub_node = self.node_subtree_group(node)
			sub_node_ar = VGroup(*self.arrow_subtree_vec(node))
			sub_mid = self.node_subtree_group(mid) + VGroup(*self.arrow_subtree_vec(mid))

			p_shift = self.get_left_pos(p) - p.pos
			p_scale = self.REC_SCALE

			node_shift = p.pos - node.pos
			node_scale = 1/self.REC_SCALE

			self.update_subtree_pos_and_scale(node, p.pos, node_scale)
			self.update_subtree_pos_and_scale(p, self.get_left_pos(p), p_scale)

			arrow_shift = 0.7 * node.scale * (LEFT + DOWN)
			new_arrow = self.get_arrow(node.pos+arrow_shift, p.pos-0.5*arrow_shift, node.scale)
			arrow_shift_mid = 0.7 * p.scale * (RIGHT + DOWN)

			new_sub_p_ar = VGroup(*[ar.copy().shift(p_shift)
				.scale(p_scale, scale_tips=True, about_point=p.pos)
					for ar in self.arrow_subtree_vec(p)])
			new_sub_node_ar = VGroup(*[ar.copy().shift(node_shift)
				.scale(node_scale, scale_tips=True, about_point=node.pos)
					for ar in self.arrow_subtree_vec(node)])

			if mid is None:
				self.play(
					sub_p.animate.shift(p_shift).scale(p_scale, about_point=p.pos),
					Transform(sub_p_ar, new_sub_p_ar),
					sub_node.animate.shift(node_shift).scale(node_scale,
						about_point=node.pos),
					Transform(sub_node_ar, new_sub_node_ar),
					Transform(p.r_arrow, new_arrow)
				)
			else:
				mid_shift = self.get_right_pos(p) - mid.pos

				self.update_subtree_pos_and_scale(mid, self.get_right_pos(p), 1)

				new_arrow_mid = self.get_arrow(p.pos+arrow_shift_mid,
					mid.pos-0.5*arrow_shift_mid, p.scale)

				self.play(
					sub_p.animate.shift(p_shift).scale(p_scale, about_point=p.pos),
					Transform(sub_p_ar, new_sub_p_ar),
					sub_node.animate.shift(node_shift).scale(node_scale,
						about_point=node.pos),
					Transform(sub_node_ar, new_sub_node_ar),
					Transform(p.r_arrow, new_arrow),
					sub_mid.animate.shift(mid_shift),
					Transform(node.l_arrow, new_arrow_mid)
				)

			node.l_arrow, p.r_arrow = p.r_arrow, node.l_arrow
			p.r = mid
			node.l = p

			if p.r is not None:
				p.r.p = p

		node.p = pp
		p.p = node;

	def splay(self, splay, cur_scale, node):
		while node.p is not None:
			p = node.p
			pp = p.p
			if pp is None: # ZIG
				print("==== ZIG")
				self.focus_on_node(splay, cur_scale, p)
				self.rotate(node)
				cur_scale /= self.REC_SCALE
				break
			else:
				self.focus_on_node(splay, cur_scale, pp)
				if (pp.l == p) != (p.l == node): # ZIG-ZAG
					print("==== ZIG-ZAG")
					self.rotate(node)
					self.rotate(node)
					cur_scale /= self.REC_SCALE
					cur_scale /= self.REC_SCALE
				else: # ZIG-ZIG
					print("==== ZIG-ZIG")
					self.rotate(p)
					self.rotate(node)
					cur_scale /= self.REC_SCALE
					cur_scale /= self.REC_SCALE
		splay.root = node

	def insert_splay(self, splay, val, do_splay=True):
		pos = splay.pos.copy()
		scale = splay.scale

		if splay.root is None:
			splay.root = Node(val, pos, scale)
			self.print_node(splay.root, scale)
			return
		
		#self.camera.frame.save_state()
		node = splay.root
		while True:
			if node.val is None:
				node.val = val
				self.print_node(node, scale)
				break
			if node.val == val:
				break

			if val < node.val:
				shift = 0.7 * (scale*LEFT + scale*DOWN)
				npos = self.get_left_pos(node)
				nscale = scale * self.REC_SCALE
				if node.l is None:
					node.l = Node(None, npos, nscale)
					node.l.p = node

					# Arrow
					node.l_arrow = self.get_arrow(pos+shift, npos-0.5*shift, scale)
					self.play(Create(node.l_arrow), run_time=0.4)

				# Move camera
				self.focus_on_node(splay, scale, node.l)

				pos = npos
				scale = nscale
				node = node.l
			else:
				shift = 0.7 * (scale*RIGHT + scale*DOWN)
				npos = self.get_right_pos(node)
				nscale = scale * self.REC_SCALE
				if node.r is None:
					node.r = Node(None, npos, nscale)
					node.r.p = node

					# Arrow
					node.r_arrow = self.get_arrow(pos+shift, npos-0.5*shift, scale)
					self.play(Create(node.r_arrow), run_time=0.4)

				# Move camera
				self.focus_on_node(splay, scale, node.r)

				pos = npos
				scale = nscale
				node = node.r

		if do_splay:
			self.splay(splay, scale, node)

		#self.play(Restore(self.camera.frame))

	def construct(self):

		random.seed(1)

		plane = NumberPlane()
		#self.add(plane)

		splay = SplayTree(ORIGIN+0.5*UP, 0.5)




		self.next_section(skip_animations=True)
		for i in range(100):
			self.insert_splay(splay, random.randint(0, 999))
		self.next_section()

		self.insert_splay(splay, random.randint(0, 999))
