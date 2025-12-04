Python Adventure Quiz
    - An Interactive Educational Application for Foundational Python Learning

Abstract
  - Python Adventure Quiz is an educational software application designed to enhance foundational Python programming skills through an interactive, narrative-driven environment. Developed using Python’s Tkinter library, the system integrates multimedia elements—including animated sequences, sound effects, and dynamic text rendering—to engage learners in an immersive learning experience. The application employs a structured assessment model where users progress through challenges by demonstrating understanding of basic programming concepts. This project demonstrates the pedagogical potential of gamification in introductory computer science education.

1. Introduction
- Effective programming education often requires bridging conceptual understanding with sustained learner engagement. This project explores the integration of game-based learning methodologies with introductory   Python instruction. Python Adventure Quiz presents a narrative scenario in which users must assist a protagonist trapped inside a virtual environment. Progression is dependent on correct responses to Python-related questions, promoting both motivation and reinforcement of core programming ideas.

  The system uses Tkinter as the primary GUI framework and incorporates additional libraries—including Pygame, Pillow (PIL), OpenCV, and ImageIO—to support multimedia interactivity.

2. System Overview
   - The application is organized around a scene-based architecture, transitioning between the main menu, user identification, narrative sequences, quiz stages, help interactions, and the final ending sequence. C  ore logic, event handling, rendering, and asset management are implemented within the primary script:

   Tkinter.py – Complete source code implementing all GUI, game logic, multimedia processing, state handling, and evaluation functions.

   The user interface provides a structured flow consisting of:
  1. Prologue narrative scenes
  2. Player interaction and decision-making segments
  3. Five-stage Python quiz module
  4. Life-based fail system and progression tracking
  5. Leaderboard presentation and data storage
  6. Final narrative conclusion

3. Pedagogical Framework
  The educational design of the application is grounded in principles of gamification and constructivist learning. The quiz elements engage learners through:
  - Immediate feedback (correct or incorrect answers)
  - Consequential decision-making (lives lost for errors)
  - Goal-oriented progression (key collection)
  - Narrative reinforcement (the storyline contextualizes tasks)
  - These elements aim to increase learner motivation, improve retention, and encourage conceptual reasoning.

 4. Technical Architecture
    
4.1 Graphical User Interface
 - Implemented exclusively in Tkinter
 - Custom-drawn widgets for buttons, panels, text boxes
 - Responsive layout with full-screen support

4.2 Multimedia Processing
- Pillow (PIL) for image loading, scaling, and GIF frame extraction
- OpenCV/ImageIO for loading video-based animations
- Pygame for audio initialization and sound playback

4.3 State Management
- Discrete states track user progress (e.g., menu, prologue, quiz, help_choice, ending)
- A centralized event-handling system manages keyboard and mouse interactions

4.4 Assessment Module
- Five multiple-choice questions covering introductory Python concepts
- Scoring integrates keys collected and remaining lives
- Evaluation results are written to a local JSON file (leaderboard.json)

5. Installation and Execution
   
5.1 Software Requirements
 The following Python libraries must be installed:
  - pip install pygame pillow imageio opencv-python

5.2 Execution
 To launch the application:
  - python Tkinter.py

Users must ensure that all external media assets (images, audio files, GIFs, video animations) are placed in accessible directories as referenced in the script.  

6. Results and Discussion
The application demonstrates that blending narrative elements with educational content can enhance student engagement. Preliminary observations suggest that learners respond positively to visual storytelling and interactive sequences, which may reduce anxiety associated with assessments and promote sustained use of the tool.

The leaderboard system additionally encourages replayability and fosters a competitive yet educational environment.

7. Contributors

The development of Python Adventure Quiz was carried out by the following team:
Baniqued, Zyron Dheniel – Project Manager
Ocampo, Rhian Kate – Lead Programmer
Frias, Justine Andrei – UI/UX Designer
Pascual, Shaqckane – Researcher
Ducusin, Katherina – Documentation 

8. Conclusion
 - This project illustrates the effectiveness of combining gamification with introductory programming instruction. By embedding Python concepts within a narrative game structure, Python Adventure Quiz offers an engaging and pedagogically sound approach for learners at the beginner level. Future developments may include expanded question sets, adaptive difficulty, and integration with online data storage for broader accessibility.

