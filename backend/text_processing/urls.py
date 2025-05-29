from django.urls import path
from .views import correct_grammar_view, classify_text_view, extract_entities_view

urlpatterns = [
    path("grammar/", correct_grammar_view, name="correct_grammar"),
    path("classify/", classify_text_view, name="classify_sentence"),
    path("extract-entities/", extract_entities_view, name="extract_entities")
]