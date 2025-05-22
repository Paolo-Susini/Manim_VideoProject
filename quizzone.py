import sys
sys.path.append(".")  # Add current directory to Python path
from manim_imports_ext import *
import numpy as np
# import random
from manimlib import config
from utils import *
import cv2
from datetime import datetime

config.pixel_height = 720
config.pixel_width = 1280
config.frame_height = 7.0
config.frame_width = 12.8

class Quizzone(Scene):

    def construct(self):
        # Set up axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            width=16,
            height=16,
            depth=8
        )
        axes.set_width(FRAME_WIDTH)
        axes.center()
        # Create axis labels manually
        # x_label = Text("X").scale(0.5).next_to(axes.x_axis.get_end(), RIGHT)
        # y_label = Text("Y").scale(0.5).next_to(axes.y_axis.get_end(), UP)
        # z_label = Text("Z").scale(0.5).next_to(axes.z_axis.get_end(), OUT)
        

        self.frame.reorient(0, 90, 0, IN, 15)
        # self.frame.add_updater(lambda m, dt: m.increment_theta(dt * 3 * DEGREES))
        # self.add(axes, x_label, y_label, z_label)  

        
        state0_s = [50, 50, 30] # Initial state for the spiral trajectory
        state0_c = [50, 50, 30] # Initial state for the circular trajectory
        time_s = 50
        time = 10
        num_curves = 3
        # Initial conditions
        alpha = 0.1   # Rate of inward spiraling
        curves = VGroup()
        # Generate the spiral trajectory

        for idx in range(1, num_curves+1):
            x_c,z_c = rotate_point_2d([state0_c[0], state0_c[2]], (2*np.pi/num_curves)*idx)
            state = [x_c, state0_c[1], z_c]
            # init_points = circle_points(state, radius=20, time=10)

            x,y = rotate_point_2d(state0_s[:2], (2*np.pi/(num_curves))*idx)
            state = [x, y, state0_s[2]]
            points = generate_spiral_to_center(state, alpha, time_s)

            # points = np.concatenate((init_points, points ), axis=1)
            curve = VMobject().set_points_as_corners(axes.c2p(*points))
            curves.add(curve)

        # def scene_question(q):
            


        def image_animation(images, curves, guest):
            
            bg = ImageMobject("Images/utils/SanNiccolò_bg.jpg")
            bg.scale(4.1)
            bg.stretch(dim=0, factor=1.1)
            bg.rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            bg.move_to(axes.get_origin() + np.array([0, 0, 3]))
            self.play(FadeIn(bg))

            # Adding scene title
        
            # Create text that will follow the curve
            text = Text(R"LAUREA HAPPELLIKKIO!", font_size=100)
            text.set_stroke(width=4)  
            text.set_color(RED)
            # text.font = "Arial"
            text.rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            text.move_to(axes.get_origin() + np.array([0, 0, 8]))
            text.set_backstroke(width=6, color=BLACK)

            self.play(*[Write(text)], run_time = 2)

            choice = images[np.random.choice([0, 1, 2])] ## Randomly select an image from the list --> the one who has to answer the question            
            
            # Set up the images
            for image in images:
                image.scale(0.8)
                image.rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            
            # self.add(images)
            self.play(images[0].animate.scale(2).move_to(axes.get_origin()))
            self.play(images[0].animate.move_to(axes.get_origin() + np.array([7, 0, 0])))

            self.play(images[1].animate.scale(2).move_to(axes.get_origin()))
            self.play(images[1].animate.move_to(axes.get_origin() + np.array([-7, 0, 0])))

            self.play(images[2].animate.scale(2).move_to(axes.get_origin()))
            self.wait()

            # Create an animation to smoothly pass from the first curves (circular) to the second curves (spiral)
            self.play(
                *[images[idx].animate.move_to(curves[idx].get_start()).scale(0.5) for idx in range(len(curves))],
                run_time=1
            )
            

            # Animate the images to follow the curves
            def animate_images(images = images, curves = curves):
                for image, curve in zip(images, curves):
                    image.move_to(curve.get_end())
            images.add_updater(animate_images) 
            
            self.bring_to_front(images)

            curves.set_opacity(0)
            # self.bring_to_back(treasure_chest)
            self.play(
                        *[anim for curve, image in zip(curves, images)
                        for anim in (ShowCreation(curve, run_time=time, rate_func=linear), 
                                    image.animate.scale(0.01))],
                        # FadeIn(treasure_chest),
                        run_time=time,
                        lag_ratio=0.7  # Adjust this value (0-1) to control overlap timing
                    )

            # Background Images 
            background = ImageMobject("Images/utils/backgound_questions3.png")
            background.set_opacity(0.5)
            background.scale(8.0)
            background.stretch(dim=0, factor=1.1)
            background.rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            background.move_to(axes.get_origin() + np.array([0, 0, 3]))
            self.bring_to_back(background)
            
            # Create the question text
            question = make_multiline_text(guest.question, max_chars=35, line_spacing=0.5).scale(1.5)
            question.set_stroke(width=4)
            question.move_to(axes.get_origin() + np.array([0, 0, 7])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            question.set_backstroke(width=5, color=BLACK)

            ## Create the answer text
            ans_a = Text(str(f"A: {guest.answers["A"]}")).scale(1.6).move_to(axes.get_origin() + np.array([0, 0, 3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            ans_b = Text(str(f"B: {guest.answers["B"]}")).scale(1.6).move_to(axes.get_origin() + np.array([0, 0, 3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            ans_c = Text(str(f"C: {guest.answers["C"]}")).scale(1.6).move_to(axes.get_origin() + np.array([0, 0, 3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            ans_d = Text(str(f"D: {guest.answers["D"]}")).scale(1.6).move_to(axes.get_origin() + np.array([0, 0, 3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            ans_a.set_stroke(width=2.5)
            ans_b.set_stroke(width=2.5)
            ans_c.set_stroke(width=2.5)
            ans_d.set_stroke(width=2.5)
            ans_a.set_backstroke(width=4, color=BLACK)
            ans_b.set_backstroke(width=4, color=BLACK)
            ans_c.set_backstroke(width=4, color=BLACK)
            ans_d.set_backstroke(width=4, color=BLACK)
                
            
            
            # Create the right answer text
            right_ans = make_multiline_text(guest.answers[guest.right_answer], max_chars=15, line_spacing=0.5).scale(4).move_to(axes.get_origin() + np.array([0, 0, 3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            right_ans.set_stroke(width=4)
            right_ans.set_backstroke(width=5, color=BLACK)
            resize_image(input_path=os.path.join("Images/guests_img", f"{guest.name}.png"),
                         output_path=os.path.join("Images/guests_img_resized", f"{guest.name}.png"),
                         quality=95)
            
            # Load the image
            guest_img = ImageMobject(os.path.join("Images/guests_img_resized", f"{guest.name}.png")).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
            # guest_name = Text(str(guest.name)).rotate(np.deg2rad(90), axis=np.array([1, 0, 0])).scale(1.5).move_to(axes.get_origin() + np.array([0, 0, -3]))
            resize_image(input_path=os.path.join("Images","Explainations", f"{guest.name}.png"),
                         output_path=os.path.join("Images","Explainations_resized", f"{guest.name}.png"),
                         width=800,
                         height=800,
                         quality=95)
            self.wait()

            # Load the explaination image
            guest_expl = ImageMobject(os.path.join("Images","Explainations_resized", f"{guest.name}.png")).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))

            
            self.play(*[FadeOut(image) for image in images.remove(choice)])
            self.remove(curves)

            # Animate the choice image
            self.add(choice)
            self.play(choice.animate.scale(400).move_to(axes.get_origin() + np.array([0, 0, 2.5])), run_time = 3),

            self.play(
                *[FadeOut(bg), FadeOut(text), choice.animate.scale(0.28).move_to(np.array([11.6, 0, 4.8])), FadeIn(background)], run_time=2)

            quiz_time_img = ImageMobject("Images/utils/quiz_time.png").rotate(np.deg2rad(90), axis=np.array([1, 0, 0])).scale(0.8).move_to(axes.get_origin() + np.array([0, 0, 3])) # Quiz Time text image
            self.play(FadeIn(quiz_time_img), run_time = 2)
            self.wait()
            self.play(quiz_time_img.animate.move_to(np.array([-9, 0, -7])).scale(0.45), run_time = 1)

            self.play(guest_img.animate.scale(3))
            self.wait()
            self.play(guest_img.animate.scale(0.3).move_to(np.array([11.6, 0, -6.8])))

            self.play(*[FadeIn(question)], run_time=2)
            self.wait(2)

            # Show the answers
            self.play(*[FadeIn(ans_a.move_to(np.array([0, 0, 0.0])))], run_time=1) 
            self.play(*[FadeIn(ans_b.move_to(np.array([0, 0, -1.6])))], run_time = 1)
            self.play(*[FadeIn(ans_c.move_to(np.array([0, 0, -3.2])))], run_time=1)
            self.play(*[FadeIn(ans_d.move_to(np.array([0, 0, -4.8])))], run_time = 1) 
            
            # self.wait(5)
            # ====== TIMER INTEGRATION ======
            # Create timer (aligned with your X-Z plane)
            five = Text("5", font_size=100).set_color(WHITE).move_to(axes.get_origin() + np.array([0, 0, -3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0])).set_stroke(width=4)
            four = Text("4", font_size=100).set_color(YELLOW_A).move_to(axes.get_origin() + np.array([0, 0, -3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0])).set_stroke(width=4)
            three = Text("3", font_size=100).set_color(YELLOW_C).move_to(axes.get_origin() + np.array([0, 0, -3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0])).set_stroke(width=4)
            two = Text("2", font_size=100).set_color(ORANGE).move_to(axes.get_origin() + np.array([0, 0, -3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0])).set_stroke(width=4)
            one = Text("1", font_size=100).set_color(RED_D).move_to(axes.get_origin() + np.array([0, 0, -3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0])).set_stroke(width=4)
            zero = Text("0", font_size=100).set_color(RED).move_to(axes.get_origin() + np.array([0, 0, -3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0])).set_stroke(width=4)
            timer = VGroup(five, four, three, two, one, zero)
            
            self.play(*[Transform(timer[0], timer[1])], run_time = 1)
            self.remove(timer)
            self.play(*[Transform(timer[1], timer[2])], run_time = 1)
            self.remove(timer)
            self.play(*[Transform(timer[2], timer[3])], run_time = 1)
            self.remove(timer)
            self.play(*[Transform(timer[3], timer[4])], run_time = 1)
            self.remove(timer)
            self.play(*[Transform(timer[4], timer[5])], run_time = 1)
            self.remove(timer)
            
            self.play(*[FadeOut(k) for k in [ans_a, ans_b, ans_c, ans_d, question]])
        
            self.play(guest_expl.animate.scale(2.8).move_to(axes.get_origin() + np.array([0, 0, 3])), run_time = 2)
            self.wait(2)

            # self.play(*[right_ans.animate.move_to(np.array([6, -1, -2])).scale(0.7), guest_expl.animate.scale(2.8).move_to(np.array([-4, 0, -2])), FadeOut(question)], run_time = 2)
            self.play(*[FadeOut(guest_expl)], run_time = 2)

            self.play(FadeIn(right_ans), run_time = 1)
            self.wait()

            # Hard coding the right answer for Alice
            if guest.name == "alice" or guest.name == "alice.pkl":
                self.wait(2)
                self.play(*[FadeOut(right_ans)], run_time = 2)
                fake_ans = Text("04/03/03").scale(4).move_to(axes.get_origin() + np.array([0, 0, 3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
                fake_ans.set_stroke(width=4)
                fake_ans.set_backstroke(width=5, color=BLACK)
                
                t = Text("SCHERZETTO :)").scale(4).move_to(axes.get_origin() + np.array([0, 0, 3])).rotate(np.deg2rad(90), axis=np.array([1, 0, 0]))
                t.set_stroke(width=4)
                t.set_backstroke(width=5, color=BLACK)
                self.play(FadeIn(t), run_time = 1)
                self.play(*[FadeOut(t)])
                self.wait()
                self.play(*[FadeIn(fake_ans)], run_time = 2)
                self.wait()
                self.play(*[FadeOut(k) for k in [fake_ans, background, guest_img, choice, quiz_time_img]])
            
            else:
                
                self.play(*[FadeOut(k) for k in [right_ans, background, guest_img, choice, quiz_time_img]])       

            return
        
        # for i, g in enumerate(glob.glob("Guests/*.pkl")):
        pickle_files = [f for f in os.listdir("Guests") if f.endswith('.pkl')] # List all .pkl files in the directory 

        # Create 3 separate pools, each containing numbers 0-39
        pools = [np.arange(40), np.arange(40), np.arange(40)]
    
        now = datetime.now()  # Get current time

        # Extract as integers
        current_hour = now.hour        # Hour (0-23)
        current_minute = now.minute    # Minute (0-59)
        current_second = now.second    # Second (0-59)
        np.random.seed(current_hour + current_minute + current_second)  # Seed the random number generator

        selected_guests = np.random.choice(pickle_files, size=len(pickle_files), replace=False) # Randomly select guests without replacement

        for g in selected_guests:
        # for g in ["pavel.pkl"]:
        
            print(f"\nLoading guest: {g}")
            guest_ = load_guest(g, directory="Guests")
            
            # Select one number from each pool (without replacement)
            chosen_list = []
            for i in range(3):  # Loop over each pool
                chosen = np.random.choice(pools[i], size=1, replace=False)  # Pick 1 number
                chosen_list.append(chosen[0])
                pools[i] = np.setdiff1d(pools[i], chosen)  # Remove it from its pool

            # Assign selections to n, l, h
            n = chosen_list[0] if 'chosen' in locals() else None  # Fallback if not chosen
            l = chosen_list[1] if len(chosen_list) > 1 else None
            h = chosen_list[2] if len(chosen_list) > 2 else None

            # print(f"Chosen number: {n}, {l}, {h}")
            # Resize images
            resize_image(f"Images/CCC/Nikki_{n}.jpg", f"Images/CCC_resized/Nikki_{n}.jpg", quality=95)
            resize_image(f"Images/CCC/Lello_{l}.jpg", f"Images/CCC_resized/Lello_{l}.jpg", quality=95)
            resize_image(f"Images/CCC/Happa_{h}.jpg", f"Images/CCC_resized/Happa_{h}.jpg", quality=95)

            # Group images
            images = Group(
                ImageMobject(f"Images/CCC_resized/Nikki_{n}.jpg"),
                ImageMobject(f"Images/CCC_resized/Lello_{l}.jpg"),
                ImageMobject(f"Images/CCC_resized/Happa_{h}.jpg"),
            )
            
            # Animate
            image_animation(images, curves, guest_)

