from manim import *
import numpy as np


class FourierDecomposition(Scene):
    def construct(self):

        MAIN_COLOR = BLUE_C
        COMPONENT_COLORS = [RED_C, GREEN_C, YELLOW_C, PURPLE_C]

        time_tracker = ValueTracker(0)

        def complex_wave(x, t):
            y = (
                0.55 * np.sin(6 * x + 2.8 * t)
                + 0.35 * np.sin(11 * x - 2.0 * t)
                + 0.20 * np.sin(18 * x + 1.5 * t)
                + 0.12 * np.sin(27 * x - 3.2 * t)
            )
            y += 0.25 * np.sin(2 * x + 0.7 * t)
            return y

        main_axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=1.6,
            axis_config={"include_ticks": False},
            tips=False,
        ).move_to(UP * 3.2)

        main_graph = always_redraw(
            lambda: main_axes.plot(
                lambda x: complex_wave(x, time_tracker.get_value()),
                x_range=[0, 10],
                color=MAIN_COLOR,
                stroke_width=3,
            )
        )

        main_label = Text("Complex EEG Signal", font_size=22).next_to(main_axes, LEFT, buff=0.15)

        component_axes = VGroup()
        component_graphs = VGroup()
        wave_labels = VGroup()

        freqs = [12, 8, 5, 2]
        amps = [0.5, 0.4, 0.32, 0.25]
        speeds = [3.0, 2.2, 1.6, 0.8]
        labels = ["β Wave", "α Wave", "θ Wave", "δ Wave"]

        wave_y_positions = [1.5, 0.4, -0.7, -1.8]

        for i in range(4):
            ax = Axes(
                x_range=[0, 10, 1],
                y_range=[-1, 1, 1],
                x_length=10,
                y_length=0.85,
                axis_config={"include_ticks": False},
                tips=False,
            ).move_to(DOWN * (wave_y_positions[0] - wave_y_positions[i]) + UP * (3.2 - 1.75) + DOWN * (i * 1.1))

            component_axes.add(ax)

            graph = always_redraw(
                lambda i=i, ax=ax: ax.plot(
                    lambda x: amps[i] * np.sin(freqs[i] * x + speeds[i] * time_tracker.get_value()),
                    x_range=[0, 10],
                    color=COMPONENT_COLORS[i],
                    stroke_width=2.5,
                )
            )
            component_graphs.add(graph)

            lbl = Text(labels[i], font_size=18, color=COMPONENT_COLORS[i]).next_to(ax, LEFT, buff=0.15)
            wave_labels.add(lbl)

        bars = VGroup()
        for i in range(4):
            bar = always_redraw(
                lambda i=i: Rectangle(
                    width=0.35,
                    height=0.8 + 0.35 * np.sin(2 * time_tracker.get_value() + i),
                    fill_color=COMPONENT_COLORS[i],
                    fill_opacity=0.9,
                    stroke_width=0,
                ).move_to(RIGHT * (4.7 + i * 0.5) + DOWN * (1.0 + i * 0.02))
            )
            bars.add(bar)

        spectrum_label = Text("Frequency Spectrum", font_size=20).next_to(bars, DOWN, buff=0.15)

        title = Text("Fourier Transform Visualization", font_size=32).to_edge(UP, buff=0.1)

        self.play(Write(title))
        self.play(Create(main_axes), Write(main_label), run_time=1.5)
        self.play(Create(main_graph), run_time=2)
        self.wait(2)

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(component_axes[i]),
                        Create(component_graphs[i]),
                        Write(wave_labels[i]),
                    )
                    for i in range(4)
                ],
                lag_ratio=0.25,
            ),
            run_time=3,
        )

        self.play(FadeIn(bars), Write(spectrum_label), run_time=1.5)

        self.play(
            time_tracker.animate.set_value(40),
            run_time=20,
            rate_func=linear
        )

        self.wait(2)