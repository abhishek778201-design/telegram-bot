"""HTML report generator for quiz scores."""
import os
from jinja2 import Template


class HTMLReportGenerator:
    """Generates self-contained HTML scorecard reports."""

    def __init__(self, theme: str = "light"):
        self.theme = theme

    def generate_report(self, quiz_data: dict, user_results: dict) -> str:
        """Generate an interactive HTML scorecard."""
        template = self._get_template()
        return template.render(
            quiz=quiz_data,
            results=user_results,
            theme=self.theme,
        )

    def generate_pdf_report(self, html_content: str, output_path: str) -> str:
        """Generate PDF report from HTML content."""
        try:
            from weasyprint import HTML
            HTML(string=html_content).write_pdf(output_path)
            return output_path
        except ImportError:
            raise RuntimeError("WeasyPrint not installed for PDF generation")

    def _get_template(self) -> Template:
        """Get HTML template for scorecard."""
        template_str = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Quiz Scorecard - {{ quiz.title }}</title>
            <style>
                :root {
                    --primary: #3b82f6;
                    --danger: #ef4444;
                    --success: #22c55e;
                    --warning: #f59e0b;
                    --bg: #ffffff;
                    --text: #1f2937;
                    --border: #e5e7eb;
                }
                {% if theme == "dark" %}
                :root {
                    --bg: #1f2937;
                    --text: #f3f4f6;
                    --border: #4b5563;
                }
                {% endif %}
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }
                .card { background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 24px; max-width: 800px; margin: 0 auto; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
                .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px solid var(--border); padding-bottom: 16px; }
                .score { font-size: 48px; font-weight: bold; color: var(--primary); }
                .question-nav { margin-top: 20px; display: flex; flex-wrap: wrap; gap: 8px; }
                .q-btn { padding: 8px 12px; border: 1px solid var(--border); border-radius: 6px; cursor: pointer; font-size: 14px; }
                .q-btn.correct { background: var(--success); color: white; border-color: var(--success); }
                .q-btn.wrong { background: var(--danger); color: white; border-color: var(--danger); }
                .q-btn.pending { background: var(--warning); color: white; border-color: var(--warning); }
                .question-detail { margin-top: 20px; padding: 16px; background: #f9fafb; border-radius: 8px; }
                .markdown-content { line-height: 1.6; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <h1>{{ quiz.title }}</h1>
                    <div class="score">{{ results.score }} / {{ results.total }}</div>
                </div>
                <p><strong>Percentage:</strong> {{ results.percentage }}%</p>
                <p><strong>Time Taken:</strong> {{ results.time_taken }}s</p>
                <div class="question-nav">
                    {% for q in quiz.questions %}
                    <button class="q-btn {% if q.correct %}correct{% elif q.attempted == False %}pending{% else %}wrong{% endif %}">Q{{ loop.index }}</button>
                    {% endfor %}
                </div>
                <div class="question-detail">
                    <h3>Question Analysis</h3>
                    <div class="markdown-content">{{ results.analysis | safe }}</div>
                </div>
            </div>
        </body>
        </html>
        """
        return Template(template_str)