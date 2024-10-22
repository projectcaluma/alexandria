import json
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser
from django.test.client import RequestFactory

from alexandria.core.models import File
from alexandria.core.views import SearchViewSet

# This is needed to disable the warning about not verifying the SSL certificate.
# It spams the output otherwise.
if not settings.ALEXANDRIA_S3_VERIFY:
    import urllib3

    urllib3.disable_warnings()


class Command(BaseCommand):
    help = "Search for content using the regular search endpoint"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("term", type=str, nargs="*")
        parser.add_argument(
            "--format",
            "-f",
            type=str,
            choices=["json", "text"],
            default="text",
            required=False,
        )
        parser.add_argument(
            "--results",
            "-n",
            type=int,
            default=10,
            required=False,
        )

    def handle(self, *args, **options):
        search_term = " ".join(options["term"])

        if options["verbosity"] > 1:
            self.stderr.write(f"Django setup complete. Searching: {search_term}")
        view = SearchViewSet.as_view({"get": "list"})
        rf = RequestFactory()

        rq = rf.get(
            "/api/v1/search",
            {
                "filter[query]": search_term,
                "page[number]": 1,
                "page[size]": options["results"],
            },
        )

        if options["verbosity"] > 1:
            self.stderr.write("Starting query now")

        started = datetime.now()
        resp = view(rq)
        if options["verbosity"] > 1:
            self.stderr.write("Query completed, results coming")
        done = datetime.now()

        output_fn = {"text": self.show_result_text, "json": self.show_result_json}

        output_fn[options["format"]](resp.data, duration=done - started)

    def show_result_text(self, data, duration):
        print(f"Query duration: {duration}")
        if "results" not in data or not data["results"]:
            print("No results")
            return
        for rec in data["results"]:
            # rank is float(0..1), map this to something user-understandable
            rank = int((rec["search_rank"] or 0) * 1000) / 10

            context = (
                rec["search_context"]
                .replace("<b>", "<<<")
                .replace("</b>", ">>>")
                .replace("\n", " ")
            )

            self.stdout.write(f"* {rec['document_title']} (R: {rank})")
            self.stdout.write(f"  {context}")
            self.stdout.write(
                f"  http://localhost/api/v1/documents/{rec['document']['id']}"
            )

        self.stdout.write("\nQuery info:")
        self.stdout.write(f"  Duration: {duration}")
        total_searched = File.objects.filter(variant="original").count()
        self.stdout.write(f"  Total searched: {total_searched}")

    def show_result_json(self, data, duration):
        self.stdout.write(
            json.dumps(
                {
                    "results": data["results"],
                    "info": {
                        "query_duration": str(duration),
                        "total_searched": File.objects.filter(
                            variant="original"
                        ).count(),
                    },
                },
                indent=4,
            )
        )
