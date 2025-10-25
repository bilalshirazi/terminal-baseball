#!/usr/bin/env python3
"""
Interactive Terminal Baseball Game
A fun baseball game with batting, pitching, and score tracking!
"""

import random
import time
from enum import Enum
from dataclasses import dataclass
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich import box
from rich.align import Align


console = Console()


class PitchType(Enum):
    FASTBALL = "Fastball"
    CURVEBALL = "Curveball"
    SLIDER = "Slider"
    CHANGEUP = "Changeup"


class SwingTiming(Enum):
    EARLY = "early"
    PERFECT = "perfect"
    LATE = "late"
    NO_SWING = "no swing"


class HitResult(Enum):
    STRIKE = "Strike"
    BALL = "Ball"
    FOUL = "Foul Ball"
    SINGLE = "Single"
    DOUBLE = "Double"
    TRIPLE = "Triple"
    HOME_RUN = "Home Run"
    OUT = "Out"
    GROUND_OUT = "Ground Out"
    FLY_OUT = "Fly Out"
    DOUBLE_PLAY = "Double Play"


@dataclass
class GameState:
    inning: int = 1
    top_of_inning: bool = True  # True = away team batting, False = home team batting
    outs: int = 0
    strikes: int = 0
    balls: int = 0
    home_score: int = 0
    away_score: int = 0
    runners: dict = None  # {1: bool, 2: bool, 3: bool}

    def __post_init__(self):
        if self.runners is None:
            self.runners = {1: False, 2: False, 3: False}

    def reset_count(self):
        self.strikes = 0
        self.balls = 0

    def clear_bases(self):
        self.runners = {1: False, 2: False, 3: False}

    def next_batter(self):
        self.reset_count()

    def record_out(self):
        self.outs += 1
        self.reset_count()
        if self.outs >= 3:
            self.next_inning()

    def next_inning(self):
        self.outs = 0
        self.clear_bases()
        self.reset_count()
        if self.top_of_inning:
            self.top_of_inning = False
        else:
            self.top_of_inning = True
            self.inning += 1


class BaseballGame:
    def __init__(self, player_name: str = "Player"):
        self.player_name = player_name
        self.computer_name = "Computer"
        self.state = GameState()
        self.player_hits = 0
        self.player_at_bats = 0
        self.computer_hits = 0
        self.computer_at_bats = 0

    def display_field(self):
        """Display the baseball field with runners"""
        field = Text()

        # Diamond display
        runner_2 = "●" if self.state.runners[2] else "○"
        runner_3 = "●" if self.state.runners[3] else "○"
        runner_1 = "●" if self.state.runners[1] else "○"

        field_art = f"""
              {runner_2}
             ╱ ╲
            ╱   ╲
          {runner_3}     {runner_1}
           ╲   ╱
            ╲ ╱
             ◆
        """

        return Panel(
            field_art,
            title="[bold cyan]Baseball Diamond[/bold cyan]",
            border_style="green"
        )

    def display_scoreboard(self):
        """Display the current score and game state"""
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("Team", style="cyan", width=15)
        table.add_column("Score", justify="center", style="yellow", width=8)

        # Highlight current batting team
        if self.state.top_of_inning:
            away_name = f"[bold green]{self.player_name}[/bold green]"
            away_score = f"[bold green]{self.state.away_score}[/bold green]"
            home_name = self.computer_name
            home_score = str(self.state.home_score)
        else:
            away_name = self.player_name
            away_score = str(self.state.away_score)
            home_name = f"[bold green]{self.computer_name}[/bold green]"
            home_score = f"[bold green]{self.state.home_score}[/bold green]"

        table.add_row(away_name, away_score)
        table.add_row(home_name, home_score)

        return table

    def display_game_info(self):
        """Display inning, outs, balls, strikes"""
        inning_half = "Top" if self.state.top_of_inning else "Bottom"

        info = Table.grid(padding=1)
        info.add_column(style="cyan", justify="right")
        info.add_column(style="yellow")

        info.add_row("Inning:", f"{inning_half} of {self.state.inning}")
        info.add_row("Outs:", f"{'●' * self.state.outs}{'○' * (3 - self.state.outs)}")
        info.add_row("Balls:", f"{'●' * self.state.balls}{'○' * (4 - self.state.balls)}")
        info.add_row("Strikes:", f"{'●' * self.state.strikes}{'○' * (3 - self.state.strikes)}")

        return Panel(info, title="[bold]Game Info[/bold]", border_style="blue")

    def display_full_game_state(self):
        """Display complete game state"""
        console.clear()
        console.print("\n")
        console.print(Align.center("[bold yellow]⚾ TERMINAL BASEBALL ⚾[/bold yellow]"))
        console.print("\n")

        # Create layout
        console.print(self.display_scoreboard())
        console.print("\n")

        # Side by side: field and info
        from rich.columns import Columns
        console.print(Columns([self.display_field(), self.display_game_info()]))
        console.print("\n")

    def pitch(self) -> PitchType:
        """Computer throws a pitch"""
        return random.choice(list(PitchType))

    def swing_or_watch(self) -> bool:
        """Player decides to swing or not"""
        choice = Prompt.ask(
            "[bold cyan]What do you do?[/bold cyan]",
            choices=["swing", "watch", "s", "w"],
            default="swing"
        )
        return choice.lower() in ["swing", "s"]

    def get_swing_timing(self) -> SwingTiming:
        """Determine swing timing (simplified random for now)"""
        rand = random.random()
        if rand < 0.25:
            return SwingTiming.EARLY
        elif rand < 0.50:
            return SwingTiming.PERFECT
        elif rand < 0.75:
            return SwingTiming.LATE
        else:
            return SwingTiming.NO_SWING

    def calculate_hit_result(self, pitch: PitchType, swung: bool, timing: SwingTiming = None) -> HitResult:
        """Calculate the result of a pitch/swing"""
        # Pitch location (simplified)
        in_zone = random.random() < 0.6  # 60% strikes

        if not swung:
            if in_zone:
                return HitResult.STRIKE
            else:
                return HitResult.BALL

        # Player swung
        if not in_zone and random.random() < 0.3:
            # Swung at ball outside zone
            return HitResult.STRIKE

        if timing == SwingTiming.PERFECT:
            # Perfect timing - high chance of hit
            rand = random.random()
            if rand < 0.15:
                return HitResult.HOME_RUN
            elif rand < 0.35:
                return HitResult.TRIPLE
            elif rand < 0.60:
                return HitResult.DOUBLE
            elif rand < 0.85:
                return HitResult.SINGLE
            else:
                return HitResult.FLY_OUT

        elif timing in [SwingTiming.EARLY, SwingTiming.LATE]:
            # Okay timing - medium chance of hit
            rand = random.random()
            if rand < 0.05:
                return HitResult.HOME_RUN
            elif rand < 0.15:
                return HitResult.DOUBLE
            elif rand < 0.35:
                return HitResult.SINGLE
            elif rand < 0.50:
                return HitResult.FOUL
            elif rand < 0.75:
                return HitResult.GROUND_OUT
            else:
                return HitResult.FLY_OUT

        else:
            # Poor contact
            rand = random.random()
            if rand < 0.20:
                return HitResult.FOUL
            elif rand < 0.60:
                return HitResult.GROUND_OUT
            else:
                return HitResult.FLY_OUT

    def advance_runners(self, bases: int):
        """Advance runners on base by a number of bases"""
        runs = 0
        new_runners = {1: False, 2: False, 3: False}

        # Move existing runners
        for base in [3, 2, 1]:  # Process from 3rd to 1st
            if self.state.runners[base]:
                new_pos = base + bases
                if new_pos > 3:
                    runs += 1  # Runner scores
                else:
                    new_runners[new_pos] = True

        # Place batter
        if bases <= 3:
            new_runners[bases] = True
        else:
            runs += 1  # Batter scores (home run)

        self.state.runners = new_runners
        return runs

    def handle_hit_result(self, result: HitResult, is_player: bool):
        """Handle the outcome of a hit"""
        runs = 0

        if result == HitResult.STRIKE:
            self.state.strikes += 1
            console.print("[red]Strike![/red]")
            if self.state.strikes >= 3:
                console.print("[bold red]Strikeout![/bold red]")
                self.state.record_out()

        elif result == HitResult.BALL:
            self.state.balls += 1
            console.print("[yellow]Ball![/yellow]")
            if self.state.balls >= 4:
                console.print("[bold yellow]Walk! Batter takes first base.[/bold yellow]")
                runs = self.advance_runners(1)
                self.state.next_batter()

        elif result == HitResult.FOUL:
            if self.state.strikes < 2:
                self.state.strikes += 1
            console.print("[yellow]Foul ball![/yellow]")

        elif result == HitResult.SINGLE:
            console.print("[bold green]Single![/bold green]")
            if is_player:
                self.player_hits += 1
            else:
                self.computer_hits += 1
            runs = self.advance_runners(1)
            self.state.next_batter()

        elif result == HitResult.DOUBLE:
            console.print("[bold green]Double![/bold green]")
            if is_player:
                self.player_hits += 1
            else:
                self.computer_hits += 1
            runs = self.advance_runners(2)
            self.state.next_batter()

        elif result == HitResult.TRIPLE:
            console.print("[bold bright_green]Triple![/bold bright_green]")
            if is_player:
                self.player_hits += 1
            else:
                self.computer_hits += 1
            runs = self.advance_runners(3)
            self.state.next_batter()

        elif result == HitResult.HOME_RUN:
            console.print("[bold bright_yellow]HOME RUN! ⚾[/bold bright_yellow]")
            if is_player:
                self.player_hits += 1
            else:
                self.computer_hits += 1
            runs = self.advance_runners(4)
            self.state.next_batter()

        elif result in [HitResult.GROUND_OUT, HitResult.FLY_OUT, HitResult.OUT]:
            console.print(f"[red]{result.value}![/red]")
            self.state.record_out()

        # Update score
        if runs > 0:
            if is_player:
                self.state.away_score += runs
            else:
                self.state.home_score += runs
            console.print(f"[bold cyan]{runs} run(s) scored![/bold cyan]")

        return runs

    def player_at_bat(self):
        """Player's turn at bat"""
        self.player_at_bats += 1

        while self.state.outs < 3 and self.state.strikes < 3 and self.state.balls < 4:
            self.display_full_game_state()

            # Pitch
            pitch = self.pitch()
            console.print(f"\n[bold yellow]Pitch incoming: {pitch.value}![/bold yellow]")
            time.sleep(0.5)

            # Player decision
            swung = self.swing_or_watch()

            if swung:
                timing = self.get_swing_timing()
                console.print(f"[cyan]Swing timing: {timing.value}[/cyan]")
                time.sleep(0.3)
            else:
                timing = None

            # Calculate result
            result = self.calculate_hit_result(pitch, swung, timing)
            time.sleep(0.3)

            # Handle result
            self.handle_hit_result(result, is_player=True)

            time.sleep(1.5)

            # Check if at-bat is over
            if result in [HitResult.SINGLE, HitResult.DOUBLE, HitResult.TRIPLE,
                         HitResult.HOME_RUN, HitResult.GROUND_OUT, HitResult.FLY_OUT]:
                break

            if self.state.strikes >= 3 or self.state.balls >= 4:
                break

    def computer_at_bat(self):
        """Computer's turn at bat (automated)"""
        self.computer_at_bats += 1

        while self.state.outs < 3 and self.state.strikes < 3 and self.state.balls < 4:
            self.display_full_game_state()

            console.print(f"\n[bold magenta]{self.computer_name} is at bat...[/bold magenta]")
            time.sleep(1)

            # Computer decision (AI)
            swung = random.random() < 0.7  # 70% chance to swing

            if swung:
                timing = random.choice([SwingTiming.EARLY, SwingTiming.PERFECT,
                                       SwingTiming.LATE, SwingTiming.PERFECT])
                console.print(f"[cyan]{self.computer_name} swings![/cyan]")
            else:
                timing = None
                console.print(f"[cyan]{self.computer_name} watches the pitch[/cyan]")

            time.sleep(0.5)

            # Calculate result (computer pitches to itself basically)
            pitch = self.pitch()
            result = self.calculate_hit_result(pitch, swung, timing)

            # Handle result
            self.handle_hit_result(result, is_player=False)

            time.sleep(1.5)

            # Check if at-bat is over
            if result in [HitResult.SINGLE, HitResult.DOUBLE, HitResult.TRIPLE,
                         HitResult.HOME_RUN, HitResult.GROUND_OUT, HitResult.FLY_OUT]:
                break

            if self.state.strikes >= 3 or self.state.balls >= 4:
                break

    def play_inning(self):
        """Play both halves of an inning"""
        # Top of inning (player bats)
        self.state.top_of_inning = True
        self.state.outs = 0
        self.state.clear_bases()

        console.print(f"\n[bold cyan]Top of inning {self.state.inning} - {self.player_name} batting[/bold cyan]")
        time.sleep(1)

        while self.state.outs < 3:
            self.player_at_bat()

        # Bottom of inning (computer bats)
        self.state.top_of_inning = False
        self.state.outs = 0
        self.state.clear_bases()

        console.print(f"\n[bold magenta]Bottom of inning {self.state.inning} - {self.computer_name} batting[/bold magenta]")
        time.sleep(1)

        while self.state.outs < 3:
            self.computer_at_bat()

    def display_final_stats(self):
        """Display final game statistics"""
        console.clear()
        console.print("\n")
        console.print(Align.center("[bold yellow]⚾ GAME OVER ⚾[/bold yellow]"))
        console.print("\n")

        # Final score
        console.print(self.display_scoreboard())
        console.print("\n")

        # Winner
        if self.state.away_score > self.state.home_score:
            console.print(Align.center(f"[bold green]{self.player_name} wins![/bold green]"))
        elif self.state.home_score > self.state.away_score:
            console.print(Align.center(f"[bold red]{self.computer_name} wins![/bold red]"))
        else:
            console.print(Align.center("[bold yellow]It's a tie![/bold yellow]"))

        console.print("\n")

        # Statistics
        stats_table = Table(title="Game Statistics", box=box.DOUBLE_EDGE)
        stats_table.add_column("Player", style="cyan")
        stats_table.add_column("At Bats", justify="center")
        stats_table.add_column("Hits", justify="center")
        stats_table.add_column("Batting Avg", justify="center", style="yellow")

        player_avg = f"{self.player_hits / max(self.player_at_bats, 1):.3f}"
        computer_avg = f"{self.computer_hits / max(self.computer_at_bats, 1):.3f}"

        stats_table.add_row(self.player_name, str(self.player_at_bats),
                           str(self.player_hits), player_avg)
        stats_table.add_row(self.computer_name, str(self.computer_at_bats),
                           str(self.computer_hits), computer_avg)

        console.print(stats_table)
        console.print("\n")

    def play(self):
        """Main game loop"""
        console.clear()
        console.print(Panel.fit(
            "[bold yellow]Welcome to Terminal Baseball![/bold yellow]\n\n"
            "Try to get hits by timing your swings correctly!\n"
            "Choose to 'swing' or 'watch' each pitch.\n\n"
            "[cyan]Commands:[/cyan]\n"
            "  swing (s) - Swing at the pitch\n"
            "  watch (w) - Let the pitch go by",
            title="⚾ Game Instructions ⚾",
            border_style="green"
        ))

        input("\nPress Enter to start the game...")

        # Play 9 innings
        for inning in range(1, 10):
            self.state.inning = inning
            self.play_inning()

        # Display final stats
        self.display_final_stats()


def main():
    """Main entry point"""
    console.clear()

    console.print(Panel.fit(
        "[bold yellow]⚾ TERMINAL BASEBALL ⚾[/bold yellow]\n\n"
        "[cyan]An interactive baseball game for your terminal![/cyan]",
        border_style="green"
    ))

    console.print("\n")
    player_name = Prompt.ask("[cyan]Enter your team name[/cyan]", default="Player")

    game = BaseballGame(player_name=player_name)
    game.play()

    console.print("\n")
    if Confirm.ask("[cyan]Play again?[/cyan]"):
        main()
    else:
        console.print("\n[yellow]Thanks for playing! ⚾[/yellow]\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Game interrupted. Thanks for playing! ⚾[/yellow]\n")
