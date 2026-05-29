from manim import *
import numpy as np
import random


class Neuron(VGroup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dendrite_terminal_lines = []

        self.soma = Circle(
            radius=0.6,
            color=BLUE,
            fill_opacity=0.3
        )

        self.nucleus = Circle(
            radius=0.18,
            color=BLUE_E,
            fill_opacity=0.8
        )

        self.dendrites = VGroup()

        for angle in np.linspace(1, TAU, 7, endpoint=False):

            branch = self.create_branch(
                start=self.soma.point_at_angle(angle),
                angle=angle,
                depth=5,
                length=1.0
            )

            self.dendrites.add(branch)

        self.axon = self.create_axon(
            start=RIGHT * 0.6,
            length=8
        )

        x_end = 8
        y_end = 0.2 * np.sin(3 * x_end)

        terminal_start = RIGHT * (0.6 + x_end) + UP * y_end

        self.axon_terminals = self.create_axon_terminals(
            terminal_start,
            depth=3
        )

        self.add(
            self.soma,
            self.nucleus,
            self.dendrites,
            self.axon,
            self.axon_terminals
        )

    def create_branch(self, start, angle, depth, length):

        end = start + np.array([
            np.cos(angle),
            np.sin(angle),
            0
        ]) * length

        line = Line(
            start,
            end,
            stroke_width=max(1.2, depth),
            color=BLUE_C
        )

        if depth == 1:

            self.dendrite_terminal_lines.append(line)

            return line

        left = self.create_branch(
            end,
            angle + random.uniform(0.3, 0.6),
            depth - 1,
            length * 0.7
        )

        right = self.create_branch(
            end,
            angle - random.uniform(0.3, 0.6),
            depth - 1,
            length * 0.7
        )

        return VGroup(line, left, right)

    def create_axon(self, start, length):

        axon_line = ParametricFunction(
            lambda t: np.array([
                t,
                0.2 * np.sin(3 * t),
                0
            ]),
            t_range=[0, length],
            color="#cc0202",
            stroke_width=4.3
        )

        axon_line.shift(start)

        self.axon_path = axon_line

        myelin = VGroup()

        for i in range(10):

            seg = RoundedRectangle(
                width=0.45,
                height=0.18,
                corner_radius=0.1,
                fill_color=WHITE,
                fill_opacity=1,
                stroke_width=0
            )

            x = 0.7 + i * 0.7
            y = 0.2 * np.sin(3 * x)

            seg.move_to(start + np.array([x, y, 0]))

            slope = 0.2 * 3 * np.cos(3 * x)

            seg.rotate(np.arctan(slope))

            myelin.add(seg)

        return VGroup(axon_line, myelin)

    def create_axon_terminals(self, start, depth=3, length=0.8):

        if depth <= 0:

            bulb = Circle(
                radius=0.06,
                fill_color=YELLOW,
                fill_opacity=1,
                stroke_width=0
            )

            bulb.move_to(start)

            return bulb

        group = VGroup()

        num_branches = random.randint(2, 3)

        for _ in range(num_branches):

            angle = random.uniform(-0.9, 0.9)

            direction = np.array([
                np.cos(angle),
                np.sin(angle),
                0
            ])

            end = start + direction * length

            branch = Line(
                start,
                end,
                color="#ebf702",
                stroke_width=max(1.2, depth)
            )

            sub = self.create_axon_terminals(
                end,
                depth=depth - 1,
                length=length * 0.7
            )

            group.add(branch, sub)

        return group


class NeuronScene(Scene):

    def get_signal_animation(self, neuron):

        terminal_branch = random.choice(
            neuron.dendrite_terminal_lines
        )

        soma_center = neuron.soma.get_center()

        particle = Dot(
            radius=0.05,
            color="#f702c2"
        )

        particle.move_to(
            terminal_branch.get_end()
        )

        incoming = MoveAlongPath(
            particle,
            terminal_branch.copy().reverse_direction(),
            rate_func=linear,
            run_time=1
        )

        to_soma = particle.animate.move_to(
            soma_center
        )

        outgoing = MoveAlongPath(
            particle,
            neuron.axon_path,
            rate_func=linear,
            run_time=2
        )

        return Succession(
            FadeIn(particle),
            incoming,
            to_soma,
            outgoing,
            FadeOut(particle)
        )

    def construct(self):

        neuron = Neuron().scale(0.9)

        neuron.shift(LEFT * 3)

        self.play(Create(neuron.soma))

        self.play(FadeIn(neuron.nucleus))

        self.play(
            LaggedStart(
                *[
                    Create(branch)
                    for branch in neuron.dendrites
                ],
                lag_ratio=0.1
            ),
            run_time=4
        )

        self.play(
            Create(neuron.axon[0]),
            run_time=3
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(seg)
                    for seg in neuron.axon[1]
                ],
                lag_ratio=0.15
            )
        )

        self.play(
            Create(neuron.axon_terminals),
            run_time=2
        )

        animations = []

        for _ in range(15):

            animations.append(
                self.get_signal_animation(neuron)
            )

        self.play(
            LaggedStart(
                *animations,
                lag_ratio=0.25
            )
        )

        self.wait(10)