from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()

def banner():


    console.print(
    Panel.fit(
        "[bold green]RNA-SEQ AUTOMATED ANALYSIS PLATFORM[/bold green]\n"
        "[cyan]One Command • Complete Analysis[/cyan]",
        border_style="green"
    )
)


def section(title):


     console.print()
     console.print(
    Rule(f"[bold cyan]{title}")
)


def success(msg):

    console.print(
    f"[bold green]✓[/bold green] {msg}"
)


def warning(msg):


    console.print(
    f"[bold yellow]⚠[/bold yellow] {msg}"
)


def error(msg):

    console.print(
    f"[bold red]✗[/bold red] {msg}"
)


def info(msg):


    console.print(
    f"[cyan]➜[/cyan] {msg}"
)


