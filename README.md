# Our repo to see if we can actually get the nao to do stuff.

## Current Status
We've got three files: one for a diving motion which we can't use. One for grabbing images which grabs them using the naoqi library and renders them using openCV. and one for tracking the ball which uses contour tracking.

## What needs to be done.
Overall the idea is to have the nao perform a set of operations where:
- The nao will only move by sidestepping along a straight line in front of the goals.
- It constantly scans for a ball
- When it finds the ball it works out if its rolling and what direction its rolling in.
- It then works out if the ball will intersect with the line it is allowed to move along, if it will intersect then it moves to the right place while tracking the ball.
