from django.shortcuts import render, redirect
from django.conf import settings
import cohere
from django.contrib.auth import login
from .forms import ContentGenerationForm, SignUpForm
from .models import GeneratedContent
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Count


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("generate_content")
    else:
        form = SignUpForm()
    return render(request, "generator/signup.html", {"form": form})


def generate_content(request):
    generated_content = None
    if request.method == "POST":
        form = ContentGenerationForm(request.POST)
        if form.is_valid():
            content_type = form.cleaned_data["content_type"]
            prompt = form.cleaned_data["prompt"]
            tone = form.cleaned_data["tone"]
            language = form.cleaned_data["language"]
            co = cohere.Client(settings.COHERE_API_KEY)
            response = co.generate(
                model="command-xlarge-nightly",
                prompt=f"Write a {content_type} in a {tone} tone in {language}: {prompt}",
                max_tokens=300,
            )
            # Get the generated content
            generated_content = response.generations[0].text.strip()
            print(generated_content)

            GeneratedContent.objects.create(
                user=request.user,
                content_type=content_type,
                prompt=prompt,
                tone=tone,
                generated_text=generated_content,
            )

    else:
        form = ContentGenerationForm()

    return render(
        request,
        "generator/content_generation.html",
        {"form": form, "generated_content": generated_content},
    )


@login_required
def content_history(request):
    content_list = GeneratedContent.objects.filter(user=request.user).order_by(
        "-created_at"
    )
    return render(
        request, "generator/content_history.html", {"content_list": content_list}
    )


def export_pdf(request, content_id):
    content = GeneratedContent.objects.get(id=content_id, user=request.user)
    template = get_template("generator/content_pdf.html")
    html = template.render({"content": content})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="content_{content_id}.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response


@login_required
def analytics(request):
    popular_types = (
        GeneratedContent.objects.values("content_type")
        .annotate(count=Count("content_type"))
        .order_by("-count")
    )
    return render(request, "generator/analytics.html", {"popular_types": popular_types})
