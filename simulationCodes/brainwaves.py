from manim import *
import numpy as np


class BrainWaveVisualization(Scene):

    def create_wave(self, axes, freq, phase, amp, color):

        glow = always_redraw(
            lambda: axes.plot(
                lambda x: amp.get_value()
                * np.sin(freq.get_value() * x + phase.get_value()),
                x_range=[0, 10],
                color=color,
                stroke_width=10,
                stroke_opacity=0.12,
                use_smoothing=False
            )
        )

        main = always_redraw(
            lambda: axes.plot(
                lambda x: amp.get_value()
                * np.sin(freq.get_value() * x + phase.get_value()),
                x_range=[0, 10],
                color=color,
                stroke_width=4,
                use_smoothing=False
            )
        )

        return VGroup(glow, main)

    def create_brain(self):

        left = ParametricFunction(
            lambda t: np.array([
                -1.2 + 0.35 * np.sin(3 * t),
                1.5 * np.sin(t),
                0
            ]),
            t_range=[-PI / 2, PI / 2],
            color=PINK,
            use_smoothing=False
        )

        right = left.copy().flip(RIGHT)

        center = Line(
            UP * 1.4,
            DOWN * 1.4,
            color=PINK,
            stroke_width=2
        )

        brain = VGroup(left, right, center)

        glow = brain.copy().set_stroke(
            width=18,
            opacity=0.08
        )

        brain.set_stroke(width=4)

        return VGroup(glow, brain)

    def construct(self):

        self.camera.background_color = "#050816"

        freq = ValueTracker(0.8)
        phase = ValueTracker(0)
        amp = ValueTracker(1)

        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_opacity": 0.06,
                "stroke_width": 1,
                "stroke_color": BLUE
            }
        )

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=3,
            axis_config={
                "include_ticks": False,
                "include_numbers": False,
                "stroke_opacity": 1.0,
                "color": WHITE
            }
        )

        axes.to_edge(RIGHT, buff=0.8)

        wave = self.create_wave(
            axes,
            freq,
            phase,
            amp,
            BLUE_C
        )

        wave2 = always_redraw(
            lambda: axes.plot(
                lambda x: 0.5 * amp.get_value()
                * np.sin(
                    freq.get_value() * x
                    + phase.get_value()
                    + 1
                ),
                x_range=[0, 10],
                color=PURPLE,
                stroke_width=2,
                stroke_opacity=0.3,
                use_smoothing=False
            )
        )

        brain = self.create_brain()
        brain.scale(1.4)
        brain.to_edge(LEFT, buff=1)

        title = Text(
            "DELTA WAVES",
            font_size=34,
            color=BLUE_B
        )

        state = Text(
            "Deep Sleep",
            font_size=26,
            color=GRAY_B
        )

        freq_label = Text(
            "0.8 Hz",
            font_size=22,
            color=GRAY_A
        )

        title.to_edge(DOWN, buff=1.4)
        state.next_to(title, DOWN, buff=0.25)
        freq_label.next_to(state, DOWN, buff=0.2)

        self.play(
            FadeIn(grid),
            FadeIn(brain),
            FadeIn(axes),
            FadeIn(wave),
            FadeIn(wave2),
            FadeIn(title),
            FadeIn(state),
            FadeIn(freq_label),
            run_time=1
        )

        stages = [
            {
                "freq": 0.8,
                "amp": 1,
                "title": "DELTA WAVES",
                "state": "Deep Sleep",
                "color": BLUE_B,
                "phase": 6,
                "pulse_color": BLUE_B
            },
            {
                "freq": 1.8,
                "amp": 0.9,
                "title": "THETA WAVES",
                "state": "Meditation",
                "color": PURPLE_B,
                "phase": 8,
                "pulse_color": PURPLE_B
            },
            {
                "freq": 3,
                "amp": 0.8,
                "title": "ALPHA WAVES",
                "state": "Relaxed Focus",
                "color": TEAL_A,
                "phase": 10,
                "pulse_color": TEAL_A
            },
            {
                "freq": 6,
                "amp": 0.7,
                "title": "BETA WAVES",
                "state": "Active Thinking",
                "color": ORANGE,
                "phase": 14,
                "pulse_color": ORANGE
            },
            {
                "freq": 11,
                "amp": 0.55,
                "title": "GAMMA WAVES",
                "state": "Cognition",
                "color": YELLOW,
                "phase": 20,
                "pulse_color": YELLOW
            }
        ]

        for s in stages:

            new_title = Text(
                s["title"],
                font_size=34,
                color=s["color"]
            ).move_to(title)

            new_state = Text(
                s["state"],
                font_size=26,
                color=GRAY_B
            ).move_to(state)

            new_freq_label = Text(
                f"{s['freq']} Hz",
                font_size=22,
                color=GRAY_A
            ).move_to(freq_label)

            self.play(
                FadeOut(title, shift=UP * 0.1),
                FadeOut(state, shift=UP * 0.1),
                FadeOut(freq_label, shift=UP * 0.1),
                run_time=0.15
            )

            title.become(new_title)
            state.become(new_state)
            freq_label.become(new_freq_label)

            self.play(
                FadeIn(title, shift=UP * 0.1),
                FadeIn(state, shift=UP * 0.1),
                FadeIn(freq_label, shift=UP * 0.1),
                run_time=0.15
            )

            brain_inner = brain[1]

            pulse_anims = Succession(
                *[
                    AnimationGroup(
                        brain_inner.animate.set_stroke(color=s["pulse_color"]).scale(1.04),
                        run_time=0.4,
                        rate_func=there_and_back
                    )
                    for _ in range(12)
                ]
            )

            self.play(
                freq.animate.set_value(s["freq"]),
                amp.animate.set_value(s["amp"]),
                phase.animate.increment_value(s["phase"]),
                pulse_anims,
                run_time=10,
                rate_func=linear
            )

        self.wait(1)