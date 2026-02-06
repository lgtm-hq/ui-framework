() => {
  const signals: string[] = [];
  const h1 = document.querySelector("h1");
  if (h1) signals.push("h1:" + h1.textContent!.trim().substring(0, 60));
  signals.push("title:" + document.title);
  const active = document.querySelector('[aria-current="page"], nav .active, nav .is-active');
  if (active) signals.push("nav:" + active.textContent!.trim().substring(0, 40));
  return signals;
};
