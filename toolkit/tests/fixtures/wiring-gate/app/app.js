// app.js — the fixture app's named handler symbols. res-1 resolves each element's
// data-handler to one of these and requires a NON-EMPTY body (§6.3-res-1). Every function
// here has a real body; a non-empty no-op would also pass res-1 (T-22 — res-1 is a static
// check, non-vacuity is res-3/E2E's job). The empty-body / missing-symbol cases the gate
// REJECTS are exercised by the F-007 negative fixtures, not present here.

const state = { email: "", password: "", name: "", code: "", showPassword: false, recovery: false };

function navigate(hash) {
  window.location.hash = hash;
}

async function post(path, body) {
  return fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
}

// ---- transient field-entry handlers (action: input) ----
function onEmailInput(e) {
  state.email = e.target.value;
}

function onPasswordInput(e) {
  state.password = e.target.value;
}

function onNameInput(e) {
  state.name = e.target.value;
}

function onNewPasswordInput(e) {
  state.password = e.target.value;
}

function onConfirmPasswordInput(e) {
  state.confirm = e.target.value;
}

function onCodeInput(e) {
  state.code = e.target.value;
}

// ---- toggles (action: toggle) ----
function onTogglePasswordVisibility() {
  state.showPassword = !state.showPassword;
}

function onToggleRecoveryMode() {
  state.recovery = !state.recovery;
}

// ---- navigations (action: navigate) ----
function goToResetRequest() {
  navigate("#/reset-request");
}

function goToLogin() {
  navigate("#/login");
}

function goToRegister() {
  navigate("#/register");
}

// ---- submits (action: submit; each hits its declared endpoint) ----
function submitSignIn() {
  return post("/api/auth/login", { email: state.email, password: state.password });
}

function submitCreateAccount() {
  return post("/api/auth/register", { email: state.email, name: state.name, password: state.password });
}

function submitEmailCode() {
  return post("/api/auth/verify", { code: state.code });
}

function submitResend() {
  return post("/api/auth/resend", { email: state.email });
}

function submitVerify() {
  return post("/api/auth/2sv/verify", { code: state.code });
}

function submitSendReset() {
  return post("/api/auth/reset/request", { email: state.email });
}

function submitUpdatePassword() {
  return post("/api/auth/reset/confirm", { password: state.password });
}
