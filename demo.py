#!/usr/bin/env python3
"""
Demo of the Baseball Game - Simulates a few at-bats automatically
"""

from baseball_game import BaseballGame, HitResult
from rich.console import Console
import time

console = Console()

def demo_game():
    """Run a demo of the baseball game"""
    console.clear()
    console.print("\n[bold yellow]⚾ TERMINAL BASEBALL - DEMO MODE ⚾[/bold yellow]\n")
    console.print("[cyan]Running automated demo to show game mechanics...[/cyan]\n")
    time.sleep(2)

    # Create game
    game = BaseballGame(player_name="Demo Team")

    console.print("[green]Game initialized![/green]")
    console.print(f"[cyan]Playing: {game.player_name} vs {game.computer_name}[/cyan]\n")
    time.sleep(1)

    # Show initial state
    game.display_full_game_state()
    time.sleep(2)

    # Simulate a few pitches
    console.print("\n[bold yellow]Simulating some at-bats...[/bold yellow]\n")
    time.sleep(1)

    # At-bat 1: Single
    console.print("[bold cyan]At-Bat 1:[/bold cyan]")
    game.display_full_game_state()
    console.print("[yellow]Pitch: Fastball[/yellow]")
    time.sleep(0.5)
    console.print("[cyan]Player swings with perfect timing![/cyan]")
    time.sleep(0.5)
    runs = game.advance_runners(1)
    game.state.next_batter()
    console.print("[bold green]SINGLE! Runner on first![/bold green]\n")
    time.sleep(2)

    # At-bat 2: Double
    console.print("[bold cyan]At-Bat 2:[/bold cyan]")
    game.display_full_game_state()
    console.print("[yellow]Pitch: Curveball[/yellow]")
    time.sleep(0.5)
    console.print("[cyan]Player swings with perfect timing![/cyan]")
    time.sleep(0.5)
    runs = game.advance_runners(2)
    if runs > 0:
        game.state.away_score += runs
        console.print(f"[bold cyan]{runs} run(s) scored![/bold cyan]")
    game.state.next_batter()
    console.print("[bold green]DOUBLE! Runner on second![/bold green]\n")
    time.sleep(2)

    # At-bat 3: Home Run
    console.print("[bold cyan]At-Bat 3:[/bold cyan]")
    game.display_full_game_state()
    console.print("[yellow]Pitch: Slider[/yellow]")
    time.sleep(0.5)
    console.print("[cyan]Player swings with PERFECT timing![/cyan]")
    time.sleep(0.5)
    runs = game.advance_runners(4)
    if runs > 0:
        game.state.away_score += runs
        console.print(f"[bold cyan]{runs} run(s) scored![/bold cyan]")
    game.state.next_batter()
    console.print("[bold bright_yellow]HOME RUN! ⚾ All runners score![/bold bright_yellow]\n")
    time.sleep(2)

    # Show final state
    game.display_full_game_state()

    console.print("\n[bold green]Demo complete![/bold green]")
    console.print("\n[yellow]To play the full interactive game, run:[/yellow]")
    console.print("[cyan]python baseball_game.py[/cyan]")
    console.print("\n[dim]Note: The full game requires an interactive terminal[/dim]\n")

if __name__ == "__main__":
    demo_game()
