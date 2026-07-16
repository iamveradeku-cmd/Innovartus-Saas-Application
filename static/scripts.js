// ============================================================================
// Innovartus — Front-end interactivity
// ============================================================================

document.addEventListener("DOMContentLoaded", () => {
  initMobileNav();
  initReservationForm();
  initNewsletterForm();
  setMinReservationDate();
});

/* ---------------------------------------------------------------------- */
/* Mobile nav toggle                                                       */
/* ---------------------------------------------------------------------- */
function initMobileNav() {
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");

  toggle.addEventListener("click", () => links.classList.toggle("open"));

  links.querySelectorAll("a").forEach((link) =>
    link.addEventListener("click", () => links.classList.remove("open"))
  );
}

/* ---------------------------------------------------------------------- */
/* Prevent picking a date in the past                                      */
/* ---------------------------------------------------------------------- */
function setMinReservationDate() {
  const dateInput = document.getElementById("date");
  const today = new Date().toISOString().split("T")[0];
  dateInput.min = today;
}

/* ---------------------------------------------------------------------- */
/* Reservation form — client validation + AJAX submit                      */
/* ---------------------------------------------------------------------- */
function initReservationForm() {
  const form = document.getElementById("reserveForm");
  const messageBox = document.getElementById("reserveMessage");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearErrors();
    messageBox.textContent = "";
    messageBox.className = "reserve__message";

    const payload = {
      name: form.name.value.trim(),
      email: form.email.value.trim(),
      phone: form.phone.value.trim(),
      guests: form.guests.value,
      date: form.date.value,
      time: form.time.value,
    };

    const submitBtn = form.querySelector(".reserve__submit");
    const originalLabel = submitBtn.querySelector(".btn__label").textContent;
    submitBtn.disabled = true;
    submitBtn.querySelector(".btn__label").textContent = "Confirming…";

    try {
      const res = await fetch("/api/reserve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();

      if (!res.ok) {
        showErrors(data.errors || {});
        messageBox.textContent = "Please correct the fields above.";
        messageBox.classList.add("error");
      } else {
        messageBox.textContent = data.message;
        messageBox.classList.add("success");
        form.reset();
        setMinReservationDate();
      }
    } catch (err) {
      messageBox.textContent = "Something went wrong. Please call us to reserve.";
      messageBox.classList.add("error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.querySelector(".btn__label").textContent = originalLabel;
    }
  });
}

function showErrors(errors) {
  Object.entries(errors).forEach(([field, message]) => {
    const el = document.getElementById(`err-${field}`);
    if (el) el.textContent = message;
  });
}

function clearErrors() {
  document.querySelectorAll(".field__error").forEach((el) => (el.textContent = ""));
}

/* ---------------------------------------------------------------------- */
/* Newsletter form (front-end only demo)                                   */
/* ---------------------------------------------------------------------- */
function initNewsletterForm() {
  const form = document.getElementById("newsletterForm");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const input = form.querySelector("input");
    input.value = "";
    input.placeholder = "Thank you — you're on the list!";
    setTimeout(() => (input.placeholder = "Your email"), 3000);
  });
}
