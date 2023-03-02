# Q-Learning based Autonomous Car Game

### Milestones:

1. Make track (done)
2. Make Car class (done)
3. Make Human playable Car (done)
4. Add Collision Detection (done)
5. Add Radar/Lidar based distance metric (done)
6. Add Reward Gates (done)
	1. Draw reward gates for the map on Canva individually to make it sequential in future(done)
	2. Draw them over the track in python (done)
7. Make Reward Gates Sequential (done)
8. Add Ai controlled Car object (done)
9. Add Q-Learning on the AI (done... poor results as of now)
	1. Tune hyperparameters (in progress)
		1. Reduce the number of radars from the car drastically to save cost on the Q-Table (done)
		2. Remove the ability to reverse(kept breaking). (After 5k epochs, it had learned to reverse lmfaooo) (done)
	2. Replace randomized learning with humanized learning (learn by seeing what a human will do in that situation) (done)
	3. Add epsilon (exploration rate per gate) (done)
	4. Combine randomized Learning to take over humanized learning base model. (done)
	5. Add a maximum time allowed to roam around before reaching a reward gate. (done)
	3. DO MORE... (running as of now)
10. Add Deep Q-Learning