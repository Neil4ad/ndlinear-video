from manim import *
from manim.utils.tex_templates import TexTemplate
from manim import Flash 
import random

# Set resolution for YouTube (1920x1080)
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_height = 6.0
config.frame_width = 10.67

helvetica_template = TexTemplate()
helvetica_template.add_to_preamble(r"\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}")
config.tex_template = helvetica_template 

class NdLinearBranding:
    """Centralized branding system for consistent colors and typography"""
    
    # Brand Colors - Corrected Ensemble palette
    PRIMARY = "#00e7c8"      # Ensemble light teal (main brand color)
    SECONDARY = "#1e8fef"    # Ensemble light blue
    ACCENT = "#4050dc"       # Ensemble dark blue
    PROBLEM = "#e74c3c"      # Red for highlighting problems
    BACKGROUND = "#111111"   # Dark background
    TEXT = "#ffffff"         # White text for contrast

    # Font sizes
    FONT_HERO = 50           # Big text that appears and shrinks
    FONT_TITLE = 32          # Section headers
    FONT_SUBTITLE = 24       # Secondary headers
    FONT_LABEL = 18          # Labels, annotations
    FONT_CONTENT = 14        # Body text

    # Typography helpers using Helvetica (enables text symbols like \textbullet)
    @staticmethod
    def title_text(text, font_size=None, color=None, **kwargs):
        if not any(cmd in text for cmd in ["\\", "$", "\\begin"]):
            text = f"\\textsf{{{text}}}"
        return Tex(
            text,
            font_size=font_size or NdLinearBranding.FONT_TITLE,
            color=color or NdLinearBranding.TEXT,
            **kwargs
        )

    @staticmethod
    def body_text(text, font_size=None, color=None, **kwargs):
        if not any(cmd in text for cmd in ["\\", "$", "\\begin"]):
            text = f"\\textsf{{{text}}}"
        return Tex(
            text,
            font_size=font_size or NdLinearBranding.FONT_CONTENT,
            color=color or NdLinearBranding.TEXT,
            **kwargs
        )


    @staticmethod
    def bullet_list(items, font_size=None, color=None, align_x=None, buff=0.05):
        """Create an aligned bullet list using standard body text"""
        bullets = VGroup(*[
            NdLinearBranding.body_text(f"\\textbullet\\quad {item}", font_size=font_size, color=color)
            for item in items
        ])
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=buff)
        if align_x is not None:
            bullets.align_to([align_x, 0, 0], LEFT)
        return bullets

#IntroScene
class Scene01_Introduction(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera.background_color = NdLinearBranding.BACKGROUND
        
    def create_data_cube(self):
        cube = Cube(side_length=2, fill_opacity=0.1, stroke_width=1)
        sections = VGroup()
        colors = [
            NdLinearBranding.PRIMARY,
            NdLinearBranding.SECONDARY,
            NdLinearBranding.ACCENT,
            "#f9a620",
            "#ffd449",
            "#1ab6a1",
        ]
        grid_size = 4
        cell_size = 2/grid_size
        for i in range(grid_size):
            for j in range(grid_size):
                for k in range(grid_size):
                    cell = Cube(
                        side_length=cell_size * 0.8,
                        fill_color=colors[(i+j+k) % len(colors)],
                        fill_opacity=0.7,
                        stroke_width=0.5,
                        stroke_color=WHITE
                    )
                    x = (i - grid_size/2 + 0.5) * cell_size
                    y = (j - grid_size/2 + 0.5) * cell_size  
                    z = (k - grid_size/2 + 0.5) * cell_size
                    cell.move_to([x, y, z])
                    sections.add(cell)
        return VGroup(cube, sections)
    
    def construct(self):
        title = NdLinearBranding.title_text(
            r"\textbf{Almost all data is multi-dimensional}",
            font_size=NdLinearBranding.FONT_HERO
        )

        title[0][15:37].set_color(NdLinearBranding.PRIMARY)
        title.to_edge(UP, buff=0.6)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=2)
        
        # VOICEOVER: Introduce the fundamental concept that most AI data is multi-dimensional
        self.wait(4.5)

        example_texts = [
            "Images: Width $\\times$ Height $\\times$ Channels",
            "Videos: Time $\\times$ Width $\\times$ Height $\\times$ Channels", 
            "Point Clouds: Points $\\times$ Features",
           # "Tabular: Rows $\\times$ Features",
            "..."
        ]
        example_colors = [
            NdLinearBranding.PRIMARY,
            NdLinearBranding.SECONDARY,
            "#1ab6a1",
            NdLinearBranding.ACCENT,
            NdLinearBranding.ACCENT
        ]
        examples = VGroup()
        start_position = title.get_center() + DOWN*1.5
        for i, (text, color) in enumerate(zip(example_texts, example_colors)):
            example = NdLinearBranding.body_text(text, font_size=NdLinearBranding.FONT_SUBTITLE, color=color)
            example.move_to(start_position + DOWN*i*0.45)
            example.align_to(LEFT*3, LEFT)
            self.add_fixed_in_frame_mobjects(example)
            self.play(FadeIn(example, shift=UP*0.3), run_time=0.8)
            examples.add(example)
            self.wait(0.3)
        
        # VOICEOVER: Explain each data type example as it appears
        self.wait(3.0)

        self.play(
            FadeOut(examples),
            title.animate.scale(0.7).to_edge(UP, buff=0.3),
            run_time=1.5
        )
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        logo = ImageMobject("ensemblelogo.png").scale(0.1)
        logo.to_corner(DR, buff=0.3)
        self.add_fixed_in_frame_mobjects(logo)
        self.play(FadeIn(logo), run_time=1.5)
        self.wait(0.5)
        data_cube = self.create_data_cube()
        self.play(FadeIn(data_cube, scale=0.8), run_time=2)
        
        # VOICEOVER: Transition to the core problem - why do we flatten this structured data?
        self.wait(1.5)

        question_text = NdLinearBranding.title_text(
            "So why do AI models keep flattening it?", 
            font_size=NdLinearBranding.FONT_SUBTITLE,
            color=NdLinearBranding.PROBLEM
        )
        question_text.move_to(title.get_center() + DOWN*0.5)
        self.add_fixed_in_frame_mobjects(question_text)
        self.play(Write(question_text), run_time=1.5)
        
        # VOICEOVER: Pose the central question that motivates NdLinear
        self.wait(1.5)

        self.play(
            data_cube.animate.scale(0.5).move_to([-.4, -0.4, 1]),
            run_time=1
        )
        cube_label = NdLinearBranding.body_text(
            "3D Tensor", 
            font_size=NdLinearBranding.FONT_LABEL,
            color=NdLinearBranding.TEXT
        )
        cube_label.move_to([-.1, .1, 0])
        self.add_fixed_in_frame_mobjects(cube_label)
        self.play(Write(cube_label), run_time=1)

        CENTER_X = 0
        COLUMN_DISTANCE = 2.8
        LEFT_COLUMN_X = CENTER_X - COLUMN_DISTANCE
        RIGHT_COLUMN_X = CENTER_X + COLUMN_DISTANCE
        BULLET_ALIGN_LEFT_X = LEFT_COLUMN_X - 1.2
        BULLET_ALIGN_RIGHT_X = RIGHT_COLUMN_X - 1.2
        ARROW_START_Y = 1
        ARROW_END_Y = -0.2
        TITLE_Y = -0.3
        VISUAL_Y = -.7
        LABEL_Y = -1.1
        BULLET_START_Y = -1.5
        BULLET_SPACING = .05

        left_arrow = Arrow(
            start=np.array([-0.8, ARROW_START_Y, 0]),
            end=np.array([LEFT_COLUMN_X, ARROW_END_Y, 0]),
            color=NdLinearBranding.PROBLEM,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.15
        )
        right_arrow = Arrow(
            start=np.array([0.8, ARROW_START_Y, 0]),
            end=np.array([RIGHT_COLUMN_X, ARROW_END_Y, 0]),
            color=NdLinearBranding.ACCENT,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.15
        )
        self.add_fixed_in_frame_mobjects(left_arrow, right_arrow)
        self.play(
            GrowArrow(left_arrow),
            GrowArrow(right_arrow),
            run_time=1.5
        )
        traditional_title = NdLinearBranding.title_text(
            "Traditional Linear", 
            font_size=NdLinearBranding.FONT_SUBTITLE,
            color=NdLinearBranding.PROBLEM
        )
        traditional_title.move_to([LEFT_COLUMN_X, TITLE_Y, 0])
        self.add_fixed_in_frame_mobjects(traditional_title)
        
        ndlinear_title = NdLinearBranding.title_text(
            "NdLinear", 
            font_size=NdLinearBranding.FONT_SUBTITLE,
            color=NdLinearBranding.ACCENT
        )
        ndlinear_title.move_to([RIGHT_COLUMN_X, TITLE_Y, 0])
        self.add_fixed_in_frame_mobjects(ndlinear_title)

        traditional_title.align_to(ndlinear_title, DOWN)

        self.play(
            Write(traditional_title),
            Write(ndlinear_title),
            run_time=1
        )
        flattened_vector = Arrow(
            start=np.array([LEFT_COLUMN_X - 0.8, VISUAL_Y, 0]),
            end=np.array([LEFT_COLUMN_X + 0.8, VISUAL_Y, 0]),
            color=NdLinearBranding.PROBLEM,
            fill_opacity=0.8,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.2
        )
        self.add_fixed_in_frame_mobjects(flattened_vector)
        vector_label = NdLinearBranding.body_text(
            "Flattened Vector", 
            font_size=NdLinearBranding.FONT_LABEL, 
            color=WHITE
        )
        vector_label.move_to([LEFT_COLUMN_X, LABEL_Y, 0])
        self.add_fixed_in_frame_mobjects(vector_label)
        
        problem_items = NdLinearBranding.bullet_list(
            items=[
                "Spatial relationships must be relearned",
                "Parameter inefficient"
            ],
            font_size=NdLinearBranding.FONT_CONTENT,
            color=WHITE,
            align_x=BULLET_ALIGN_RIGHT_X
        )

        problem_items.move_to([BULLET_ALIGN_LEFT_X + 0.3, BULLET_START_Y, 0])
        self.add_fixed_in_frame_mobjects(problem_items)

        dim_cubes = VGroup()
        cube_colors = [NdLinearBranding.PRIMARY, NdLinearBranding.SECONDARY, NdLinearBranding.ACCENT]
        cube_spacing = 0.4
        for i, color in enumerate(cube_colors):
            small_cube = Cube(side_length=0.25, fill_color=color, fill_opacity=0.8, stroke_width=1)
            small_cube.rotate(PI/6, axis=UP)
            small_cube.rotate(PI/8, axis=RIGHT)
            cube_x = RIGHT_COLUMN_X + (i-1) * cube_spacing
            small_cube.move_to([cube_x, VISUAL_Y, 0])
            dim_cubes.add(small_cube)
        self.add_fixed_in_frame_mobjects(dim_cubes)
        cubes_label = NdLinearBranding.body_text(
            "Axis-wise Processing", 
            font_size=NdLinearBranding.FONT_LABEL, 
            color=WHITE
        )
        cubes_label.move_to([RIGHT_COLUMN_X, LABEL_Y, 0])
        self.add_fixed_in_frame_mobjects(cubes_label)

        solution_items = NdLinearBranding.bullet_list(
            items=[
                "Spatial structures are preserved",
                "Parameter efficiency reduces overhead",
                "Open-source",
                "A drop-in replacement for nn.linear layers"
            ],
            font_size=NdLinearBranding.FONT_CONTENT,
            color=WHITE,
            align_x=RIGHT_COLUMN_X - 1.2
        )

        # Keep the same x-position (right column), but match the vertical alignment
        solution_items.move_to([RIGHT_COLUMN_X, problem_items.get_top()[1] - 0.35, 0])
        self.add_fixed_in_frame_mobjects(solution_items)
        
        self.play(
            GrowArrow(flattened_vector),
            Write(vector_label),
            Write(problem_items),
            FadeIn(dim_cubes),
            Write(cubes_label),
            Write(solution_items),
            run_time=2
        )
        
        # VOICEOVER: Explain the key differences between traditional and NdLinear approaches
        self.wait(2.5)

        tagline = NdLinearBranding.title_text(
            r"\textbf{Same computation, efficient design}",
            font_size=NdLinearBranding.FONT_SUBTITLE,
            color=NdLinearBranding.PRIMARY
        )
        
        tagline[0][16:23].set_color(NdLinearBranding.SECONDARY)
        tagline.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(tagline)
        self.play(Write(tagline), run_time=1.5)
        
        # VOICEOVER: Emphasize the key value proposition
        self.wait(2.0)

#SCENE 2: FLATTENING PROBLEMS 
class Scene02_FlatteningProblems(Scene):
    def construct(self):
        self.camera.background_color = NdLinearBranding.BACKGROUND
        
        # Title
        title = NdLinearBranding.title_text("Why Flattening Causes Problems")
        title.to_edge(UP, buff=0.3)        
        self.play(Write(title), run_time=0.8)
        
        # VOICEOVER: Let's dive deeper into why flattening is problematic
        self.wait(1.0)

        # Create text lines
        intro_line1 = NdLinearBranding.body_text(
            "Flattening introduces two critical problems:", font_size=24
        )
        # Tight vertical spacing for intro lines
        intro = VGroup(intro_line1).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        bullet1 = NdLinearBranding.body_text(
            "1. Loss of Spatial Structure", font_size=24, color=NdLinearBranding.PROBLEM
        )
        bullet2 = NdLinearBranding.body_text(
            "2. Parameter Explosion", font_size=24, color=NdLinearBranding.PROBLEM
        )
        bullets = VGroup(bullet1, bullet2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        # Full block
        block = VGroup(intro, bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        block.align_to(LEFT * 3, LEFT)
        block.shift(RIGHT * 0.7)
        block.to_edge(UP, buff=1.8)

        # Add text instantly instead of writing
        self.add(intro_line1)
        self.wait(0.2)
        self.play(FadeIn(bullet1), run_time=0.6)
        self.wait(0.2)
        self.play(FadeIn(bullet2), run_time=0.6)
        
        # VOICEOVER: Introduce the two main problems we'll examine
        self.wait(1.5)
        
        # Structure Loss Visualization
        # Create a more clear section subtitle
        structure_title = NdLinearBranding.title_text("Problem 1: Loss of Spatial Structure", font_size=32, color=NdLinearBranding.PROBLEM)
        structure_title.next_to(title, DOWN, buff=0.6)
        
        # Fade out intro and bullets as we show the first problem
        self.play(
            FadeOut(intro),
            FadeOut(bullets),
            FadeIn(structure_title),
            run_time=0.7
        )
        
        # VOICEOVER: First, let's examine how spatial structure is lost
        self.wait(1.0)
        
        # Grid of 4x4 with "256" labels
        grid = VGroup()
        grid_size = 4
        box_size = 0.5
        grid_spacing = 0.1  # Space between grid cells
        
        for row in range(grid_size):
            for col in range(grid_size):
                box = Rectangle(
                    width=box_size, 
                    height=box_size, 
                    fill_color=NdLinearBranding.SECONDARY, 
                    fill_opacity=0.8, 
                    stroke_width=1.5, 
                    stroke_color=WHITE
                )
                
                # Position in a grid with spacing
                box.move_to(np.array([
                    (col - grid_size/2 + 0.5) * (box_size + grid_spacing),
                    (grid_size/2 - row - 0.5) * (box_size + grid_spacing),
                    0
                ]) + np.array([0, 0.7, 0]))  # Shifted up to create space between grid and vector
                
                label = NdLinearBranding.body_text("256", font_size=14)
                label.move_to(box.get_center())
                cell = VGroup(box, label)
                grid.add(cell)
        
        # Create a boxed explanation to the left of the grid
        grid_explanation = NdLinearBranding.body_text(
            "Feature maps: $4\\times 4$ spatial grid\\\\with 256 channels at each location",
            font_size=20
        )
        
        # Create background box for the explanation
        grid_explanation_bg = SurroundingRectangle(
            grid_explanation,
            color=NdLinearBranding.SECONDARY,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=1.5,
            buff=0.15
        )
        
        # Group the explanation and its background
        grid_explanation_group = VGroup(grid_explanation_bg, grid_explanation)
        
        # Position to the left of the grid with some vertical alignment
        grid_explanation_group.next_to(grid, LEFT, buff=0.6)
        grid_explanation_group.align_to(grid, UP)
        grid_explanation_group.shift(DOWN * 0.5)  # Adjusted vertical alignment
        
        # Fix #1: FadeOut structure_title when grid appears
        self.play(
            FadeIn(grid), 
            FadeOut(structure_title),
            run_time=0.8
        )
        
        # Add explanation box after grid appears
        self.play(
            FadeIn(grid_explanation_group),
            run_time=0.7
        )
        
        # VOICEOVER: Here we have feature maps - a 4x4 spatial grid with 256 channels at each location
        self.wait(2.0)
        
        # Create dots to represent the grid cells for the animation
        dots = VGroup()
        for cell in grid:
            dot = Dot(point=cell.get_center(), color=NdLinearBranding.SECONDARY, radius=0.08)
            dots.add(dot)
        
        # Create the flattened vector representation
        vector_start_x = -4  # Left side of the screen
        vector_length = 8    # Length of the vector
        vector_y = -0.8      # Position lowered to create more space
        
        # Create an arrowheaded line instead of a plain line
        vector_line = Arrow(
            start=[vector_start_x, vector_y, 0],
            end=[vector_start_x + vector_length, vector_y, 0],
            buff=0,  # No buffer to ensure the line starts and ends at the specified points
            color=WHITE,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.05  # Smaller arrowhead
        )
        
        vector_label = NdLinearBranding.body_text("Flattened Vector ($4 \\times 4 \\times 256 = 4096$ values)", font_size=20)
        vector_label.next_to(vector_line, DOWN, buff=0.3)
        
        # Animate the transition from grid to flattened vector
        # Also fade out the explanation box as grid disappears
        self.play(
            *[FadeOut(cell) for cell in grid],
            *[FadeIn(dot) for dot in dots],
            FadeOut(grid_explanation_group),  # Fade out explanation as grid collapses
            run_time=0.8
        )
        self.wait(0.3)
        
        # Draw the vector line
        self.play(Create(vector_line), run_time=0.6)
        self.play(Write(vector_label), run_time=0.6)
        
        # VOICEOVER: During flattening, this structured grid becomes a single vector
        self.wait(1.5)
        
        # Animate dots collapsing onto the vector line
        dot_targets = []
        # Fix #3: Decrease spacing between dots to fit within vector length
        available_space = vector_length * 0.95  # Use 95% of vector length to keep dots away from arrow tip
        dot_spacing = available_space / (len(dots) - 1)  # Distribute dots evenly
        
        for i, dot in enumerate(dots):
            # Calculate position along the vector line with adjusted spacing
            target_x = vector_start_x + (i * dot_spacing)
            dot_targets.append([target_x, vector_y, 0])
        
        # Collapse animation
        self.play(
            *[dot.animate.move_to(target) for dot, target in zip(dots, dot_targets)],
            run_time=1.5  # Longer time to emphasize the collapse
        )
        
        # VOICEOVER: Adjacent elements in the grid can end up far apart in the flattened vector
        self.wait(2.0)
        
        # Show warning about structure loss
        structure_warning = NdLinearBranding.body_text(
            "Spatial structure information is lost during flattening.\\ Adjacent grid elements can end up far apart in the vector.",
            font_size=20,
            color=NdLinearBranding.PROBLEM
        )
        structure_warning.next_to(vector_line, UP, buff=1.0)
        
        warning_box = SurroundingRectangle(
            structure_warning,
            color=NdLinearBranding.PROBLEM,
            buff=0.2,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=2
        )
        
        structure_warning_group = VGroup(warning_box, structure_warning)
        
        self.play(
            FadeIn(warning_box),
            Write(structure_warning),
            run_time=0.8
        )
        
        # VOICEOVER: This destroys the spatial relationships that the CNN worked hard to learn
        self.wait(2.0)
        
        # Clear screen for the second problem
        self.play(
            FadeOut(dots),
            FadeOut(vector_line),
            FadeOut(vector_label),
            FadeOut(structure_warning_group),
            run_time=0.8
        )


#SCENE 3 TRADITIONAL LINEAR LAYER -- PARAMETER EXPLOSION
class Scene03_TraditionalCNNProblem(Scene):
    def construct(self):
        # Title
        self.camera.background_color = NdLinearBranding.BACKGROUND
        
        title = NdLinearBranding.title_text("Traditional CNN Architecture with Linear Layers")
        title.to_edge(UP, buff=0.3)
        
        self.play(Write(title), run_time=1.0)
        
        # VOICEOVER: Introduce the traditional CNN architecture
        self.wait(1.0)
        
        # ---- SIMPLIFIED LAYOUT ----
        # Create boxes with IDENTICAL heights for alignment
        box_height = 1.4
        
        # Input box with CIFAR horse image
        input_box = Square(side_length=box_height, color=WHITE, fill_opacity=0.1)
        
        # Load the actual horse image
        horse_img = ImageMobject("horse_cifar.png")
        horse_img.scale_to_fit_height(box_height * 0.85)  # Scale to fit inside the box
        horse_img.move_to(input_box.get_center())
        
        input_label = NdLinearBranding.body_text(r"Input\\$32\times32\times3$", font_size=22)
        input_label.next_to(input_box, DOWN, buff=0.1)
        
        # Use Group instead of VGroup when mixing ImageMobject with other mobjects
        input_group = Group(input_box, horse_img, input_label)
        
        # CNN block
        cnn_box = Rectangle(width=1.7, height=box_height, color=NdLinearBranding.SECONDARY, fill_opacity=0.1)
        cnn_label = NdLinearBranding.body_text(r"CNN Blocks", font_size=18)
        cnn_label.move_to(cnn_box.get_center() + UP * 0.3)
        
        # Feature map size (inside CNN box)
        feature_text = NdLinearBranding.body_text(r"Feature Maps\\$4\times4\times256$", font_size=20, color=NdLinearBranding.ACCENT)
        feature_text.move_to(cnn_box.get_center() + DOWN * 0.3)
        
        cnn_group = VGroup(cnn_box, cnn_label, feature_text)
        
        # Flatten operation
        flatten_box = Rectangle(width=1.4, height=box_height, color=WHITE, fill_opacity=0.2)
        flatten_label = NdLinearBranding.body_text(r"Flatten", font_size=20)
        flatten_label.move_to(flatten_box.get_center() + UP * 0.3)
        
        flat_diagram = NdLinearBranding.body_text(r"$\rightarrow$ 4096 values", font_size=18)
        flat_diagram.move_to(flatten_box.get_center() + DOWN * 0.3)
        
        flatten_group = VGroup(flatten_box, flatten_label, flat_diagram)
        
        # Linear layer
        linear_box = Rectangle(width=1.4, height=box_height, color=NdLinearBranding.TEXT, fill_opacity=0.2)
        linear_label = NdLinearBranding.body_text(r"Linear\\Layer", font_size=20)
        linear_label.move_to(linear_box)
        linear_group = VGroup(linear_box, linear_label)
        
        # Output
        output_box = Rectangle(width=1.4, height=box_height, color=NdLinearBranding.PROBLEM, fill_opacity=0.3)
        output_label = NdLinearBranding.body_text(r"Output\\10 classes", font_size=20)
        output_label.move_to(output_box)
        output_group = VGroup(output_box, output_label)
        
        # Position all elements with proper alignment
        all_boxes = [input_box, cnn_box, flatten_box, linear_box, output_box]
        all_groups = [input_group, cnn_group, flatten_group, linear_group, output_group]
        
        # Group everything to apply scaling
        main_group = Group()
        for group in all_groups:
            main_group.add(group)
        
        main_group.shift(UP * 0.25)

        # Scale down the entire layout
        main_group.scale(0.85)
        
        # Calculate spacing between elements
        total_width = config.frame_width
        content_width = sum(box.width for box in all_boxes)
        num_spaces = len(all_boxes) - 1
        
        # Calculate spacing to fill available width with margins
        margin = 1.0  # Margin on each side
        available_width = total_width - (2 * margin) - content_width
        space_width = available_width / num_spaces
        
        # Position first element with left margin
        all_groups[0].to_edge(LEFT, buff=margin)
        
        # Position the rest with calculated spacing
        for i in range(1, len(all_groups)):
            all_groups[i].next_to(all_groups[i-1], RIGHT, buff=space_width)
        
        # Adjust vertical positions to center all boxes
        avg_y = np.mean([box.get_center()[1] for box in all_boxes])
        for group in all_groups:
            # Find the main box in this group
            for mob in group:
                if isinstance(mob, Rectangle) or isinstance(mob, Square):
                    # Center this box vertically
                    y_offset = avg_y - mob.get_center()[1]
                    group.shift(UP * y_offset)
                    break
        
        # Move everything up slightly to make room for parameter counter
        for group in all_groups:
            group.shift(UP * 0.4)
        
        # Parameter counter setup
        param_tracker = ValueTracker(0)
        param_number = DecimalNumber(
            0,
            num_decimal_places=0,
            group_with_commas=True,
            font_size=24,
            color=WHITE
        )
        
        def update_number(mob):
            mob.set_value(param_tracker.get_value())
            return mob
        
        param_number.add_updater(update_number)
        param_title = NdLinearBranding.body_text("Parameter Count", font_size=24)
        
        param_container = VGroup(param_title, param_number)
        param_container.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        param_container.to_edge(DOWN+LEFT, buff=0.6)

        param_bg = SurroundingRectangle(
            param_container,
            stroke_color=NdLinearBranding.PROBLEM,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.85,
            buff=0.2
        )
        
        param_group = VGroup(param_bg, param_container)
        param_group.shift(UP * 0.3)
        
        # Warning icon - initially invisible
        warning_icon = Text("⚠️", font_size=36)
        warning_icon.next_to(param_bg, RIGHT, buff=0.2)
        warning_icon.set_opacity(0)
        
        
        # Create arrows connecting components
        arrows = []
        
        for i in range(len(all_boxes) - 1):
            start_point = all_boxes[i].get_center() + RIGHT * (all_boxes[i].width / 2)
            end_point = all_boxes[i+1].get_center() + LEFT * (all_boxes[i+1].width / 2)
            
            arrow = Arrow(
                start=start_point,
                end=end_point,
                buff=0.1,
                color=WHITE
            )
            arrows.append(arrow)
        
        # Problem identification box - initially invisible
        problem_title = NdLinearBranding.body_text("Two Problems:", font_size=24, color=NdLinearBranding.PROBLEM)
        problem_1 = NdLinearBranding.body_text("1. Structure Loss", font_size=20, color=NdLinearBranding.PROBLEM)
        problem_2 = NdLinearBranding.body_text("2. Parameter Explosion", font_size=20, color=NdLinearBranding.PROBLEM)
        
        problems = VGroup(problem_title, problem_1, problem_2)
        problems.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        problems.to_edge(DOWN+RIGHT, buff=0.5)
        
        problem_bg = SurroundingRectangle(
            problems,
            stroke_color=NdLinearBranding.PROBLEM,
            stroke_width=2,
            fill_color=BLACK,
            fill_opacity=0.85,
            buff=0.2
        )
        
        problem_group = VGroup(problem_bg, problems, warning_icon)
        problem_group.set_opacity(0)  # Start invisible
        problem_group.align_to(param_group, DOWN)

        # ANIMATION SEQUENCE
        
        # 1. Show components sequentially with more time for voiceover
        self.play(FadeIn(input_group), run_time=0.7)
        
        # VOICEOVER: Explain the input - 32x32x3 CIFAR image
        self.wait(1.0)
        
        # Add parameter counter from the very beginning
        self.play(FadeIn(param_bg), FadeIn(param_container), run_time=0.7)
        self.wait(0.3)
        
        # Add boxes and light them up as arrows touch them
        self.play(FadeIn(cnn_group), run_time=0.7)
        
        # VOICEOVER: Explain CNN feature extraction process
        self.wait(1.0)
        
        # First arrow and highlight input box as source
        self.play(
            input_box.animate.set_stroke(color=NdLinearBranding.PROBLEM, width=4),
            run_time=0.4
        )
        self.play(
            GrowArrow(arrows[0]),
            run_time=0.6
        )
        # Highlight CNN box as destination and reset input box
        self.play(
            cnn_box.animate.set_stroke(color=NdLinearBranding.PROBLEM, width=4),
            input_box.animate.set_stroke(color=WHITE, width=1),
            run_time=0.4
        )
        
        # CNN parameters increase when CNN box is highlighted
        cnn_params = 120000
        self.play(param_tracker.animate.set_value(cnn_params), run_time=1.0)
        
        # VOICEOVER: Note the reasonable parameter count for CNN layers
        self.wait(1.0)
        
        self.play(FadeIn(flatten_group), run_time=0.7)
        
        # VOICEOVER: Explain flattening step - turning 4x4x256 into 4096 values
        self.wait(1.0)
        
        # Second arrow with highlighting
        self.play(
            GrowArrow(arrows[1]),
            cnn_box.animate.set_stroke(color=NdLinearBranding.SECONDARY, width=2),
            flatten_box.animate.set_stroke(color=NdLinearBranding.PROBLEM, width=4),
            run_time=0.6
        )
        
        self.play(FadeIn(linear_group), run_time=0.7)
        
        # VOICEOVER: Introduce the linear layer that will cause problems
        self.wait(1.0)
        
        # Third arrow with highlighting
        self.play(
            GrowArrow(arrows[2]),
            flatten_box.animate.set_stroke(color=WHITE, width=2),
            linear_box.animate.set_stroke(color=NdLinearBranding.PROBLEM, width=4),
            run_time=0.6
        )
        
        self.play(FadeIn(output_group), run_time=0.7)
        self.wait(0.3)
        
        # Linear layer parameters explosion - when the linear layer is highlighted
        linear_params = 950000  # To make total 1.07M
        total_params = cnn_params + linear_params  # 1.07M
        
        self.play(
            param_tracker.animate.set_value(total_params),
             Flash(param_number, color=NdLinearBranding.PROBLEM, flash_radius=0.8),
            run_time=1.4  # Longer animation to emphasize parameter explosion
        )
        
        # VOICEOVER: Emphasize the parameter explosion - from 120k to over 1M!
        self.wait(2.0)
        
        # 6. Show warning and problems when parameter counter is maxed
        self.play(
            FadeIn(warning_icon), 
            problem_group.animate.set_opacity(1),
            run_time=1
        )
        
        # VOICEOVER: Identify the two main problems this creates
        self.wait(1.5)
        
        # 7. After parameter explosion and warning, show final arrow to output
        self.play(
            GrowArrow(arrows[3]),
            linear_box.animate.set_stroke(color=NdLinearBranding.TEXT, width=2),
            output_box.animate.set_stroke(color=NdLinearBranding.PROBLEM, width=4),
            run_time=0.7
        )
        
        # VOICEOVER: Wrap up the traditional approach problems
        self.wait(2.0)

class Scene04_NdLinearSolution(Scene):

    def construct(self):
        self.camera.background_color = NdLinearBranding.BACKGROUND
        old_title = NdLinearBranding.title_text("Traditional CNN Architecture with Linear Layers", font_size=32)
        old_title.to_edge(UP, buff=0.3)

        new_title = NdLinearBranding.title_text("CNN Architecture with NdLinear", font_size=32)
        new_title.to_edge(UP, buff=0.3)

        box_height = 1.4

        # Input box with CIFAR horse image
        input_box = Square(side_length=box_height, color=WHITE, fill_opacity=0.1)
        
        # Load the actual horse image
        horse_img = ImageMobject("horse_cifar.png")
        horse_img.scale_to_fit_height(box_height * 0.85)  # Scale to fit inside the box
        horse_img.move_to(input_box.get_center())
        
        input_label = NdLinearBranding.body_text(r"Input\\$32\times32\times3$", font_size=22)
        input_label.next_to(input_box, DOWN, buff=0.1)
        
        # Use Group instead of VGroup when mixing ImageMobject with other mobjects
        input_group = Group(input_box, horse_img, input_label)
        
        # CNN block
        cnn_box = Rectangle(width=1.7, height=box_height, color=NdLinearBranding.SECONDARY, fill_opacity=0.1)
        cnn_label = NdLinearBranding.body_text(r"CNN Blocks", font_size=18)
        cnn_label.move_to(cnn_box.get_center() + UP * 0.3)
        
        # Feature map size (inside CNN box)
        feature_text = NdLinearBranding.body_text(r"Feature Maps\\$4\times4\times256$", font_size=20, color=NdLinearBranding.ACCENT)
        feature_text.move_to(cnn_box.get_center() + DOWN * 0.3)
        
        cnn_group = VGroup(cnn_box, cnn_label, feature_text)
        
        # Flatten operation
        flatten_box = Rectangle(width=1.4, height=box_height, color=WHITE, fill_opacity=0.2)
        flatten_label = NdLinearBranding.body_text(r"Flatten", font_size=20)
        flatten_label.move_to(flatten_box.get_center() + UP * 0.3)
        
        flat_diagram = NdLinearBranding.body_text(r"$\rightarrow$ 4096 values", font_size=18)
        flat_diagram.move_to(flatten_box.get_center() + DOWN * 0.3)
        
        flatten_group = VGroup(flatten_box, flatten_label, flat_diagram)
        
        # Linear layer
        linear_box = Rectangle(width=1.4, height=box_height, color=NdLinearBranding.TEXT, fill_opacity=0.2)
        linear_label = NdLinearBranding.body_text(r"Linear\\Layer", font_size=20)
        linear_label.move_to(linear_box)
        linear_group = VGroup(linear_box, linear_label)
        #Trying to fix font rendering here
        self.add(linear_label)


        flatten_linear_group = VGroup(flatten_group, linear_group)

        # OUTPUT GROUP
        output_box = Rectangle(width=1.4, height=box_height, color=NdLinearBranding.PROBLEM, fill_opacity=0.3)
        output_label = NdLinearBranding.body_text(r"Output\\10 classes", font_size=20)
        output_label.move_to(output_box)
        output_group = VGroup(output_box, output_label)
        #Font rendering fix:
        self.add(output_label)


        # LAYOUT AND ALIGNMENT
        all_groups = [input_group, cnn_group, flatten_group, linear_group, output_group]
        main_group = Group(*all_groups).arrange(RIGHT, buff=0.7)
        for group in all_groups:
            group.align_to(input_box, DOWN)
        main_group.shift(UP * 0.5)

        # OLD ARROWS (correctly aligned)
        input_box.align_to(cnn_box, DOWN)
        old_arrows = [
            Arrow(input_box.get_right(), cnn_box.get_left(), buff=0.1, color=WHITE),
            Arrow(cnn_box.get_right(), flatten_box.get_left(), buff=0.1, color=WHITE),
            Arrow(flatten_box.get_right(), linear_box.get_left(), buff=0.1, color=WHITE),
            Arrow(linear_box.get_right(), output_box.get_left(), buff=0.1, color=WHITE),
       ]

       # PARAMETER COUNTER - CENTERED
        param_tracker = ValueTracker(1048576)
        param_number = DecimalNumber(param_tracker.get_value(), num_decimal_places=0,
                                    group_with_commas=True, font_size=24, color=WHITE)
        param_number.add_updater(lambda m: m.set_value(param_tracker.get_value()))
        param_title = NdLinearBranding.body_text(r"Traditional Parameters", font_size=24)
        param_container = VGroup(param_title, param_number).arrange(DOWN, buff=0.1)
        param_container.move_to(DOWN * 1.8)  # Centered horizontally, bottom positioned
        param_bg = SurroundingRectangle(param_container, stroke_color=NdLinearBranding.SECONDARY,
                                       stroke_width=2, fill_color=BLACK, fill_opacity=0.85, buff=0.2)
        param_group = VGroup(param_bg, param_container)

        # PROBLEM GROUP FROM SCENE 2
        problem_title = NdLinearBranding.body_text(r"Two Problems:", font_size=24, color=NdLinearBranding.PROBLEM)
        problem_1 = NdLinearBranding.body_text(r"1. Structure Loss", font_size=20)
        problem_2 = NdLinearBranding.body_text(r"2. Parameter Explosion", font_size=20)
        problems = VGroup(problem_title, problem_1, problem_2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        problems.to_edge(DOWN + RIGHT, buff=0.5)
        problem_bg = SurroundingRectangle(problems, stroke_color=NdLinearBranding.PROBLEM, stroke_width=2,
                                         fill_color=BLACK, fill_opacity=0.85, buff=0.2)
        problem_group = VGroup(problem_bg, problems)
        problem_group.align_to(param_group, UP)
       
        # SOLVED GROUP
        solved_title = NdLinearBranding.body_text(r"Problems Solved:", font_size=24, color=NdLinearBranding.ACCENT)
        solved_1 = NdLinearBranding.body_text(r"1. Structure Preserved $\checkmark$", font_size=20)
        solved_2 = NdLinearBranding.body_text(r"2. Parameters Reduced $\checkmark$", font_size=20)
        solved = VGroup(solved_title, solved_1, solved_2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        solved.to_edge(DOWN + RIGHT, buff=0.5)
        solved_bg = SurroundingRectangle(solved, stroke_color=NdLinearBranding.ACCENT,
                                            stroke_width=2, fill_color=BLACK, fill_opacity=0.85, buff=0.2)
        solved_group = VGroup(solved_bg, solved).set_opacity(0)
        solved_group.align_to(param_group, UP)

        # NDLINEAR REPLACEMENT
        ndlinear_width = linear_box.get_right()[0] - flatten_box.get_left()[0]
        ndlinear_box = Rectangle(width=ndlinear_width, height=box_height, color=NdLinearBranding.ACCENT, fill_opacity=0.3)
        ndlinear_label = NdLinearBranding.body_text(r"NdLinear\\Layer", font_size=20)
        ndlinear_label.move_to(ndlinear_box)
        ndlinear_group = VGroup(ndlinear_box, ndlinear_label)
        ndlinear_group.move_to(flatten_linear_group.get_center())

        # NEW ARROWS
        new_arrow1 = Arrow(input_box.get_right(), cnn_box.get_left(), buff=0.1, color=WHITE)
        new_arrow2 = Arrow(cnn_box.get_right(), ndlinear_box.get_left(), buff=0.1, color=WHITE)
        new_arrow3 = Arrow(ndlinear_box.get_right(), output_box.get_left(), buff=0.1, color=WHITE)

        # CODE COMPARISON OVERLAY
        code_before = NdLinearBranding.body_text(
            r"Traditional approach\\nn.Flatten()\\nn.Linear(4096, 10)",
            font_size=16,
            color=NdLinearBranding.PROBLEM
        )
        code_after = NdLinearBranding.body_text(
            r"NdLinear drop-in\\NdLinear((4,4,256), (1,1,10))",
            font_size=16,
            color=NdLinearBranding.ACCENT
        )
        
        code_comparison = VGroup(code_before, code_after).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        code_comparison.next_to(param_group, LEFT, buff=1.0)
        code_comparison.align_to(param_group, UP)  # Align tops
        code_bg = SurroundingRectangle(
            code_comparison,
            stroke_color=WHITE,
            stroke_width=1,
            fill_color=BLACK,
            fill_opacity=0.85,
            buff=0.2
        )
        code_group = VGroup(code_bg, code_comparison).set_opacity(0)

        # REPLACE ANIMATION OVERLAY
        replace_text = NdLinearBranding.title_text("REPLACE", font_size=36, color=NdLinearBranding.PRIMARY)
        replace_text.move_to(flatten_linear_group.get_center())
        replace_text.set_opacity(0)

        # --- BEGINNING STATE ---
        self.add(old_title, main_group, *old_arrows, param_group, problem_group)
        
        # VOICEOVER: Now let's see how NdLinear solves these problems
        self.wait(2.0)

        # --- ARROWS & PROBLEM FADE OUT + TITLE CHANGE ---
        self.play(
            *[FadeOut(arrow) for arrow in old_arrows],
            FadeOut(problem_group),
            ReplacementTransform(old_title, new_title),
            run_time=1.5
        )

        # --- SHOW CODE COMPARISON ---
        self.play(
            code_group.animate.set_opacity(1),
            run_time=1.0
        )
        
        # VOICEOVER: The replacement is as simple as changing one line of code
        self.wait(2.0)

        # --- REPLACE ANIMATION WITH "REPLACE" OVERLAY ---

        self.play(
            replace_text.animate.set_opacity(1),
            run_time=0.5
        )

        self.play(
            flatten_linear_group.animate.shift(DOWN * 1.7),
            run_time=0.8
        )

        self.play(
            FadeIn(ndlinear_group),
            replace_text.animate.set_opacity(0),
            GrowArrow(new_arrow1),
            run_time=.6  # Reduced from 1.5 since we split the animation
        )
        
        self.remove(flatten_linear_group)  # Fully remove it after move

        # VOICEOVER: NdLinear replaces both flattening and linear layers in one step
        self.wait(1.5)

        # --- PARAMETER LABEL CHANGE ---
        new_param_title = NdLinearBranding.body_text(r"NdLinear Parameters", font_size=24)
        new_param_title.move_to(param_title)
        self.play(
            ReplacementTransform(param_title, new_param_title),
            param_bg.animate.set_stroke(color=NdLinearBranding.ACCENT),
            run_time=1.2
        )
        self.wait(0.3)

        # --- COUNTDOWN ---
        self.play(GrowArrow(new_arrow2), run_time=1.0)
        self.play(
            param_tracker.animate.set_value(65280),
            Flash(param_number, color=NdLinearBranding.ACCENT, flash_radius=0.8),
            run_time=2.2
        )

        # VOICEOVER: Watch the dramatic parameter reduction - from over 1M to just 65K!
        self.wait(2.0)

        # --- FINAL ARROW + SOLVED ---
        self.play(
            GrowArrow(new_arrow3), 
            solved_group.animate.set_opacity(1),
            FadeOut(code_group),  # Clean up code comparison
            run_time=1.2
        )
        
        # VOICEOVER: Both problems solved with a simple drop-in replacement
        self.wait(2.5)


class Scene05_NdLinearTransformation(ThreeDScene):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.camera.background_color = NdLinearBranding.BACKGROUND
                
            def construct(self):
                # Title
                title = NdLinearBranding.title_text("Axis-aware processing with NdLinear")
                title.to_edge(UP, buff=0.3)
                self.add_fixed_in_frame_mobjects(title)
                self.play(Write(title), run_time=0.8)
                
                # VOICEOVER: Now let's see how NdLinear processes data differently
                self.wait(1.5)
                
                # Horse image - ORIGINAL POSITIONING
                horse_img = ImageMobject("horse_cifar.png").scale(1.5)
                self.add_fixed_in_frame_mobjects(horse_img)
                self.play(FadeIn(horse_img), run_time=0.8)
                
                # VOICEOVER: Starting with our same image data
                self.wait(1.0)
                
                # Camera setup
                self.move_camera(phi=60 * DEGREES, theta=120 * DEGREES)
                
                # Cube - ORIGINAL POSITIONING
                cube = Cube(
                    side_length=1.2,
                    fill_opacity=0.5,
                    fill_color=NdLinearBranding.SECONDARY,
                    stroke_color=WHITE,
                ).move_to(ORIGIN)
                
                self.play(FadeOut(horse_img), FadeIn(cube), run_time=1.0)
                self.add(cube)
                
                # Final refined label positions - ORIGINAL POSITIONING
                height_label = NdLinearBranding.body_text("Height", font_size=22, color="#FF5555")
                height_label.move_to([1.35, -0.4, 0])
                
                width_label = NdLinearBranding.body_text("Width", font_size=22, color="#55FF55")
                width_label.move_to([1.0, 1, 0])
                
                depth_label = NdLinearBranding.body_text("Depth\\\\ (Channels)", font_size=22, color="#5555FF")
                depth_label.move_to([-1.7, -0.5, 0])
                
                self.add_fixed_in_frame_mobjects(height_label, width_label, depth_label)
                self.play(
                    FadeIn(height_label),
                    FadeIn(width_label),
                    FadeIn(depth_label),
                    run_time=1.2
                )
                
                # VOICEOVER: Instead of flattening, NdLinear preserves the 3D structure
                self.wait(2.0)
                
                # Create explanation text
                transform_text = NdLinearBranding.body_text("NdLinear transforms each dimension separately", 
                                    font_size=24)
                transform_text.to_edge(UP, buff=1.2)  # Position under title
                self.add_fixed_in_frame_mobjects(transform_text)
                self.play(FadeIn(transform_text), run_time=0.8)
                
                # VOICEOVER: The key insight is to transform each dimension independently
                self.wait(2.0)
                
                # Parameter efficiency calculation - positioned carefully to avoid overlap
                param_title = NdLinearBranding.body_text("Parameter Count Comparison:", font_size=24)

                # Create the standard linear row as a single unit
                standard_text = NdLinearBranding.body_text("Standard Linear:", font_size=14, color=NdLinearBranding.PROBLEM)
                standard_formula = NdLinearBranding.body_text("$D \\times H \\times W \\times (D' \\times H' \\times W')$",
                                            font_size=16, color=NdLinearBranding.PROBLEM)
                standard_row = VGroup(standard_text, standard_formula)
                standard_row.arrange(RIGHT, buff=0.2)

                # Create the NdLinear row as a single unit  
                ndlinear_text = NdLinearBranding.body_text("NdLinear:", font_size=14, color=NdLinearBranding.ACCENT)
                ndlinear_formula = NdLinearBranding.body_text("$(D \\times D') + (H \\times H') + (W \\times W')$",
                                            font_size=18, color=NdLinearBranding.ACCENT)
                ndlinear_row = VGroup(ndlinear_text, ndlinear_formula)
                ndlinear_row.arrange(RIGHT, buff=0.2)

                # Arrange everything vertically
                param_group = VGroup(param_title, standard_row, ndlinear_row)
                param_group.arrange(DOWN, buff=0.15, aligned_edge=LEFT)

                # Scale down if needed to fit on screen
                param_group.scale(0.9)

                # Position parameter box in bottom right 
                param_group.move_to([3.0, -1.6, 0]) 
                
                # Create background box
                param_bg = SurroundingRectangle(
                    param_group,
                    stroke_color=WHITE,
                    stroke_width=1,
                    fill_color=BLACK,
                    fill_opacity=0.7,
                    buff=0.2
                )
                
                param_display = VGroup(param_bg, param_group)
                self.add_fixed_in_frame_mobjects(param_display)
                
                # Animate parameter calculation appearance
                self.play(
                    FadeIn(param_bg),
                    Write(param_group),
                    run_time=1.2
)
                
                # VOICEOVER: Compare the parameter counts - multiplication versus addition
                self.wait(2.5)
                
                # Final output cube transformation
                output_cube = Cube(
                    side_length=1.1,  # Slightly smaller
                    fill_opacity=0.5,
                    fill_color=NdLinearBranding.PRIMARY,  # NdLinear primary color
                    stroke_color=WHITE,
                ).move_to(ORIGIN)
                
                # Output dimension labels
                output_height_label = NdLinearBranding.body_text("$H_1$", font_size=24, color="#FF5555")
                output_height_label.move_to(height_label.get_center())
                
                output_width_label = NdLinearBranding.body_text("$H_2$", font_size=24, color="#55FF55")
                output_width_label.move_to(width_label.get_center())
                
                output_depth_label = NdLinearBranding.body_text("$H_3$", font_size=24, color="#5555FF")
                output_depth_label.move_to(depth_label.get_center())
                
                self.add_fixed_in_frame_mobjects(output_height_label, output_width_label, output_depth_label)
                
                # Transition to output cube
                self.play(
                    ReplacementTransform(cube, output_cube),
                    FadeOut(height_label),
                    FadeOut(width_label),
                    FadeOut(depth_label),
                    FadeIn(output_height_label),
                    FadeIn(output_width_label),
                    FadeIn(output_depth_label),
                    run_time=1.2
                )
                
                # VOICEOVER: The output maintains the same structural organization
                self.wait(1.5)
                
                # Advantages summary - positioned in bottom left - SHIFTED UP by 0.1
                advantages = VGroup(
                    NdLinearBranding.body_text("$\\bullet$ Preserves multi-dimensional structure", font_size=18),
                    NdLinearBranding.body_text("$\\bullet$ Reduces parameter count significantly", font_size=18),
                    NdLinearBranding.body_text("$\\bullet$ Same computational complexity $O(n)$", font_size=18)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
                
                # Position advantages box in bottom left - SHIFTED UP by 0.1
                advantages.move_to([-3, 1, 0]) 
                
                advantages_box = SurroundingRectangle(
                    advantages,
                    color=NdLinearBranding.PRIMARY,  # NdLinear primary color
                    fill_color=BLACK,
                    fill_opacity=0.8,
                    buff=0.2
                )
                
                advantages_group = VGroup(advantages_box, advantages)
                self.add_fixed_in_frame_mobjects(advantages_group)
            
                # GitHub link overlay - MOVED DOWN by 0.25
                github_link = NdLinearBranding.body_text(
                "github.com/ensemble-core/NdLinear",
                font_size=18,
                color=NdLinearBranding.PRIMARY
            )
                github_link.to_edge(DOWN) 
                github_link.shift(DOWN*.27)
                self.add_fixed_in_frame_mobjects(github_link)
            
                # Final transition - replace transformation text with advantages and GitHub link
                self.play(
                    FadeOut(transform_text),
                    FadeIn(advantages_group),
                    FadeIn(github_link),
                    run_time=0.8
                )
                
                # VOICEOVER: These advantages make NdLinear a powerful drop-in replacement
                self.wait(2.0)
                
                # Add Ensemble logo at the very end - MOVED TO UPPER RIGHT
                logo = ImageMobject("ensemblelogo.png").scale(.2)  # Slightly smaller for tech content
                logo.to_corner(DL, buff=0.3) 
                self.add_fixed_in_frame_mobjects(logo)
                self.play(FadeIn(logo), run_time=1.0)
                
                
                # VOICEOVER: Visit our GitHub for the code and documentation
                self.wait(2.5)