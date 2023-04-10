import random
import pathlib
import collections

from manim import *

"""
class DefaultTemplate(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.flip(RIGHT)  # flip horizontally
        square.rotate(-3 * TAU / 8)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation
"""


class Quote(Scene):
    def construct(self):
        quote = Tex(r"""\begin{raggedright} Mathematics is like love; a simple idea,\\ 
        but it can get complicated.
        \\\end{raggedright}""", r"— Anonymous", font_size=40)

        quote[0].set_color(YELLOW)
        self.play(Write(quote, run_time=3))
        self.play(FadeOut(quote))

class ComputerPile(MovingCameraScene):
    def construct(self):
        group = Group(*[random.choice([
            SVGMobject("assets/CPUassets.svg"),
            SVGMobject("assets/GPUassets.svg"),
            SVGMobject("assets/RAMassets.svg"),
            SVGMobject("assets/6502assets.svg"),
            SVGMobject("assets/ALUassets.svg"),
            SVGMobject("assets/greenassets.svg"),
            SVGMobject("assets/jennyassets.svg"),
        ]) for i in range(100)])
        self.add(group.arrange_in_grid(cols=6))

        self.camera.frame.set_y(25)

        self.play(self.camera.frame.animate.shift(DOWN * 40.5), run_time=10)
        self.play(self.camera.frame.animate.shift(DOWN * 11), run_time=1)


class MathematiciansScene(Scene):
    def construct(self):
        Mathematician = collections.namedtuple("Mathematician", ("name", "filename"))
        mathematicians = []

        for file in pathlib.Path('assets/mathematicians').iterdir():
            mathematicians.append(
                Mathematician(' '.join(file.name.split('.')[0].split('_')),
                              str(file.absolute()))
            )

        mathematician_images = [
            Group(
                ImageMobject(mathematician.filename).scale_to_fit_height(2.5),
                Tex(mathematician.name, font_size=40)
            ).arrange(DOWN)
            for mathematician in mathematicians
        ]
        print(mathematician_images)
        mathematician_img_group = Group(*mathematician_images).arrange_in_grid(rows=2, col_widths=[3, 3])
        self.play(
            AnimationGroup(*[FadeIn(image, shift=DOWN) for image in mathematician_images], lag_ratio=.25, run_time=2))
        self.wait()

        self.play(mathematician_img_group.animate.arrange(RIGHT).shift(UP * 1.5).scale_to_fit_height(2))
        self.wait()

        question = Tex(r"""
        What are the classes of problems \\
        that computers can solve?
        """, tex_environment="flushleft").shift(DOWN)
        alt_question = Tex(r"""
        {{What}} kind of problems are practically \\
        impossible for computers to solve?
        """, tex_environment="flushleft").shift(DOWN)

        self.play(Write(question))
        self.wait()
        self.play(Transform(question, alt_question))
        self.wait()
        self.play(FadeOut(question, alt_question, mathematician_img_group, shift=UP))

        computability_table = Table(
            [
                ["Arithmetic", r"Halting Problem (determining if a\\given series of instructions "
                               r"will\\infinitely loop"],
                ["Polynomial Factoring", "General, rigorous, logical proof"],
                ["Root finding", "Extremely large prime factorization"],
                ["Graph theory...?", ""]
            ],
            element_to_mobject=lambda x: Tex(x, tex_environment="flushleft", font_size=30),
            arrange_in_grid_config={"cell_alignment": LEFT + UP},
            col_labels=[Tex("Possible for computers", color=GREEN), Tex("Practically impossible", color=RED)]
        )
        self.play(FadeIn(computability_table))


class ChurchAndTuring(Scene):
    def construct(self):
        church = Group(ImageMobject("assets/mathematicians/Alonzo_Church.jpg").scale_to_fit_width(3),
                       Tex("Alonso Church"))\
.arrange(DOWN)
        turing = Group(ImageMobject("assets/mathematicians/Alan_Turing.jpg").scale_to_fit_width(3),
                       Tex("Alan Turing"))\
            .arrange(DOWN)

        church_turing_group = Group(turing, church).arrange(LEFT)
        self.play(AnimationGroup(*[FadeIn(m, shift=DOWN) for m in [church, turing]], lag_ratio=.5))

        self.wait()

        self.play(church_turing_group.animate.arrange(DOWN).shift(LEFT * 5).scale_to_fit_width(2))
        the_strat = Tex(r"""
        \Large \textbf{The strategy}\\
        \normalsize Construct a {{highly simplified}},\\
        mathematical (a physicist might say {{\textit{“idealized”}}})\\
        model of a computer, then investigate its properties.
        """, tex_environment="flushleft", font_size=40).shift(RIGHT * 1.5)
        the_strat.set_color_by_tex("simplified", BLUE)
        the_strat.set_color_by_tex("idealized", BLUE)

        self.play(Write(the_strat, shift=DOWN, run_time=5))
        self.wait()

        rectangle = SurroundingRectangle(turing, color=WHITE)

        turing_machine_group = Group(
            ImageMobject("assets/misc/Turing_Machine.jpg"),
            Tex(r"\textit{Fig. 1} A finite, mechanical model of a Turing Machine", font_size=30)
        ).arrange(DOWN).shift(RIGHT)

        self.play(
            the_strat.animate.shift(DOWN),
            Create(rectangle),
            FadeOut(the_strat),
            FadeIn(turing_machine_group)
        )
        self.wait()

        lambda_calc_title = Tex(r"{{$\lambda$}}-calculus", font_size=120).shift(RIGHT)

        lambda_calc_subtitle = Tex(r"Modeling {{computation}} with {{functions}}", font_size=50)
        lambda_calc_subtitle.set_color_by_tex("computation", RED)
        lambda_calc_subtitle.set_color_by_tex("functions", BLUE)

        lambda_group = Group(lambda_calc_title, lambda_calc_subtitle).arrange(DOWN).shift(RIGHT)

        self.play(
            rectangle.animate.surround(church),
            AnimationGroup(Write(lambda_calc_title), FadeIn(lambda_calc_subtitle, shift=UP), lag_ratio=.75),
            FadeOut(turing_machine_group)
        )

        self.play(
            FadeOut(lambda_group, shift=UP),
            FadeOut(church_turing_group, shift=LEFT),
            FadeOut(rectangle, shift=LEFT)
        )


class Functions(Scene):
    def construct(self):
        math = MathTex("f(", "x", ")", " = ", "x^2", font_size=120)
        function_application_1 = MathTex("f({{3}}) = {{x^2}}", font_size=120)
        function_application_2 = MathTex("{{f(3)}} = {{3}}^2", font_size=120)
        function_application_3 = MathTex("{{f(3)}} = {{9}}", font_size=120)

        header = Tex("Conventional Functions").next_to(math, UP)

        input_brace = Brace(math[1])
        input_brace_label = Tex("input").next_to(input_brace, DOWN)

        output_brace = Brace(math[4])
        output_brace_label = Tex("output").next_to(output_brace, DOWN)

        self.play(
            Write(header),
            FadeIn(math, shift=UP, run_time=0.5)
        )

        self.wait()

        self.play(
            Create(input_brace),
            Write(input_brace_label),
        )

        self.wait()

        self.play(
            Create(output_brace),
            Write(output_brace_label)
        )

        self.play(TransformMatchingShapes(math, function_application_1, run_time=0.25))
        self.play(TransformMatchingTex(function_application_1, function_application_2))

        new_in_brace = Brace(function_application_3[0])
        new_out_brace = Brace(function_application_3[2])

        self.play(
            Transform(function_application_2, function_application_3),
            Transform(input_brace, new_in_brace),
            input_brace_label.animate.next_to(new_in_brace, DOWN),
            Transform(output_brace, new_out_brace),
            output_brace_label.animate.next_to(new_out_brace, DOWN)
        )
