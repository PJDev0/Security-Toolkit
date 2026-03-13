#!/usr/bin/env python3
"""
SVG Badge Generator for Security Scorecard
"""


class BadgeGenerator:
    # Shields.io-style badge templates
    TEMPLATES = {
        'flat': """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="20" role="img" aria-label="{label}: {message}">
  <title>{label}: {message}</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r">
    <rect width="{width}" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_width}" height="20" fill="#555"/>
    <rect x="{label_width}" width="{message_width}" height="20" fill="{color}"/>
    <rect width="{width}" height="20" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="110">
    <text x="{label_x}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{label_length}">{label}</text>
    <text x="{label_x}" y="140" transform="scale(.1)" textLength="{label_length}">{label}</text>
    <text x="{message_x}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{message_length}">{message}</text>
    <text x="{message_x}" y="140" transform="scale(.1)" textLength="{message_length}">{message}</text>
  </g>
</svg>""",
        
        'plastic': """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="18" role="img" aria-label="{label}: {message}">
  <title>{label}: {message}</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#fff" stop-opacity=".7"/>
    <stop offset=".1" stop-color="#aaa" stop-opacity=".1"/>
    <stop offset=".9" stop-color="#000" stop-opacity=".3"/>
    <stop offset="1" stop-color="#000" stop-opacity=".5"/>
  </linearGradient>
  <clipPath id="r">
    <rect width="{width}" height="18" rx="4" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_width}" height="18" fill="#555"/>
    <rect x="{label_width}" width="{message_width}" height="18" fill="{color}"/>
    <rect width="{width}" height="18" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="110">
    <text x="{label_x}" y="140" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{label_length}">{label}</text>
    <text x="{label_x}" y="130" transform="scale(.1)" textLength="{label_length}">{label}</text>
    <text x="{message_x}" y="140" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{message_length}">{message}</text>
    <text x="{message_x}" y="130" transform="scale(.1)" textLength="{message_length}">{message}</text>
  </g>
</svg>"""
    }
    
    COLORS = {
        'brightgreen': '#4c1',
        'green': '#97CA00',
        'yellow': '#dfb317',
        'yellowgreen': '#a4a61d',
        'orange': '#fe7d37',
        'red': '#e05d44',
        'blue': '#007ec6',
        'grey': '#555',
        'gray': '#555',
        'lightgrey': '#9f9f9f',
        'lightgray': '#9f9f9f'
    }
    
    def __init__(self, style='flat'):
        self.style = style
    
    def generate(self, label: str, message: str, color: str) -> str:
        """Generate SVG badge"""
        # Calculate text widths (approximate: 6px per char + 10px padding)
        label_length = len(label) * 60 + 20
        message_length = len(message) * 60 + 20
        label_width = label_length // 10 + 10
        message_width = message_length // 10 + 10
        
        width = label_width + message_width
        label_x = (label_width * 5) + 50
        message_x = (label_width * 10) + (message_width * 5) + 50
        
        # Get color hex
        color_hex = self.COLORS.get(color, color)
        
        template = self.TEMPLATES.get(self.style, self.TEMPLATES['flat'])
        
        return template.format(
            width=width,
            height=20 if self.style == 'flat' else 18,
            label=label,
            message=message,
            color=color_hex,
            label_width=label_width,
            message_width=message_width,
            label_x=label_x,
            message_x=message_x,
            label_length=label_length,
            message_length=message_length
        )
    
    def save(self, svg_content: str, filename: str):
        """Save SVG to file"""
        with open(filename, 'w') as f:
            f.write(svg_content)
        print(f"Badge saved to {filename}")


def generate_score_badge(score: int, max_score: int, grade: str, color: str, output_file: str = 'badge.svg'):
    """Helper to generate security score badge"""
    generator = BadgeGenerator(style='flat')
    message = f"{score}/{max_score} ({grade})"
    svg = generator.generate("security score", message, color)
    generator.save(svg, output_file)
    return output_file


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        score = int(sys.argv[1])
        max_score = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        grade = sys.argv[3] if len(sys.argv) > 3 else 'B'
        color = sys.argv[4] if len(sys.argv) > 4 else 'green'
    else:
        score, max_score, grade, color = 85, 100, 'B', 'green'
    
    generate_score_badge(score, max_score, grade, color)