function showMessage(message, isSuccess) {
    var messageDiv = isSuccess ? $("#successMessage") : $("#ErrorMessage");
    messageDiv.text(message);
    messageDiv.fadeIn("slow").delay(5000).fadeOut("slow");
}