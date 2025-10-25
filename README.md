# Terminal Baseball

An interactive baseball game for your terminal! Experience America's favorite pastime right in your command line with beautiful colors and animations.

## Features

- **Interactive Gameplay**: Choose to swing or watch each pitch
- **Full Game Simulation**: Play through 9 complete innings
- **Beautiful Terminal UI**: Colorful interface using the Rich library
- **Real Baseball Mechanics**:
  - Balls, strikes, and outs
  - Singles, doubles, triples, and home runs
  - Base runners and scoring
  - Batting statistics
- **Player vs Computer**: Compete against an AI opponent
- **Live Scoreboard**: Track the game in real-time

## Screenshots

```
⚾ TERMINAL BASEBALL ⚾

              ●
             ╱ ╲
            ╱   ╲
          ○     ●
           ╲   ╱
            ╲ ╱
             ◆
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd terminal-baseball
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install the rich library directly:
```bash
pip install rich
```

## Usage

Run the game:
```bash
python baseball_game.py
```

Or make it executable:
```bash
chmod +x baseball_game.py
./baseball_game.py
```

## How to Play

1. **Starting the Game**: Enter your team name when prompted
2. **At Bat**: Each time you're at bat, you'll see:
   - The current score
   - Baseball diamond with runners
   - Balls, strikes, and outs count
3. **Making Decisions**:
   - Type `swing` or `s` to swing at the pitch
   - Type `watch` or `w` to let the pitch go by
4. **Scoring**: Get hits to advance runners and score runs!
5. **Winning**: Have more runs than the computer after 9 innings

## Game Mechanics

### Pitching
The computer throws four types of pitches:
- Fastball
- Curveball
- Slider
- Changeup

### Hitting
Your swing timing determines the quality of contact:
- **Perfect timing**: High chance of hits (singles, doubles, triples, home runs)
- **Early/Late timing**: Medium chance of hits, more likely to get out
- **Poor contact**: Foul balls or outs

### Results
Possible outcomes for each at-bat:
- **Strike**: Missed the ball or didn't swing at a good pitch
- **Ball**: Pitch outside the strike zone (4 balls = walk to first base)
- **Foul Ball**: Hit but went foul (doesn't count as a strike if you have 2 strikes)
- **Single/Double/Triple**: Hit! Advance 1, 2, or 3 bases
- **Home Run**: Hit it out of the park! All runners score
- **Ground Out/Fly Out**: You're out!

### Base Running
- Runners automatically advance based on the hit
- Multiple runners can score on extra-base hits
- Runs are added to your score immediately

## Requirements

- Python 3.7+
- rich >= 13.0.0

## Controls

- `swing` or `s` - Swing at the pitch
- `watch` or `w` - Watch the pitch go by
- `Ctrl+C` - Quit the game

## Tips

- Don't swing at every pitch! Sometimes it's better to watch
- Walks are as good as singles for getting on base
- Perfect timing is key to getting extra-base hits
- Watch the count - with 3 balls, the next pitch might be a ball

## License

MIT License - Feel free to modify and distribute!

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Roadmap

Future enhancements could include:
- Difficulty levels
- More advanced AI
- Stealing bases
- Pitching controls
- Season/tournament mode
- Save game statistics
- Multiplayer support

Enjoy playing Terminal Baseball! ⚾
