function validateForm(formId) {
  const form = document.getElementById(formId);

  if (form) {
    form.addEventListener("submit", function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();         // Блокируем отправку
        event.stopPropagation();        // Остановим всплытие
        form.reportValidity();          // Показываем сообщение браузера
      }
    });
  }
}

window.addEventListener("DOMContentLoaded", () => {
  validateForm("modalForm");
  validateForm("footerForm");
});
