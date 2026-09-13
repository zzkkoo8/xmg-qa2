import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

const root = document.getElementById("root");

if (!root) {
  throw new Error("root element is required");
}

createRoot(root).render(
  <StrictMode>
    <main>xmg-qa2 support foundation</main>
  </StrictMode>,
);
