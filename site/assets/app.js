const state = { lang: localStorage.getItem("ll-lang") || "zh-CN", query: "", category: "all", quality: "all" };
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
const text = (item) => item?.[state.lang] ?? item?.en ?? "";
let catalog = null;

function setLanguage(lang) {
  state.lang = lang;
  localStorage.setItem("ll-lang", lang);
  document.documentElement.lang = lang;
  $$("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    el.textContent = UI[lang][key] ?? key;
  });
  $$("[data-i18n-placeholder]").forEach((el) => {
    const key = el.dataset.i18nPlaceholder;
    el.placeholder = UI[lang][key] ?? key;
  });
  $$(".lang-toggle button").forEach((button) => button.classList.toggle("active", button.dataset.lang === lang));
  $$("[data-doc-link]").forEach((link) => {
    link.href = lang === "zh-CN" ? "../docs/deployment.zh-CN.md" : "../docs/deployment.en.md";
  });
  renderCategories();
  renderSkills();
}

const UI = {
  "zh-CN": {
    navCatalog:"技能目录", navDeploy:"本地部署", navPlatform:"科研平台", navGithub:"GitHub",
    eyebrow:"本地优先 · 中英双语 · 可审计", heroTitle:"链邻学术技能仓库", heroSub:"系统化组织学术 AI 能力",
    heroLead:"覆盖从选题、检索、精读、写作到数据、实验、可视化和成果转化的完整科研流程。每项技能都有功能、环境、来源、风险和质量状态。",
    browse:"浏览全部技能", deploy:"本地部署", allSkills:"技能总数", categories:"类别", firstParty:"链邻原创", external:"固定第三方",
    whyTitle:"不是堆文件，而是建立可信技能目录", whyText:"同一入口说明每项能力能做什么、需要什么、产出什么、风险在哪里，以及验证到了哪一步。",
    p1:"双语同构", p1d:"中文和英文目录使用同一数据源生成，保证数量、分类、状态与链接一致。",
    p2:"分级质量", p2d:"区分已收录、测试版、已测试、已验证与金标，拒绝用“全部可用”掩盖证据差异。",
    p3:"来源隔离", p3d:"链邻原创与固定第三方清晰区分，第三方原始指令不被改写成链邻作品。",
    catalogTitle:"完整技能与功能目录", catalogText:"按关键词、类别和质量状态筛选。点击技能可查看双语说明与原始 SKILL.md。",
    search:"搜索技能、功能或说明", allCategories:"全部类别", allQuality:"全部质量状态",
    result:"项结果", noResult:"没有匹配的技能，请调整筛选条件。",
    platformTitle:"不想逐项安装？使用链邻科研 AI 平台", platformText:"平台面向希望开箱即用的科研用户，整合技能、模型、数据工具和工作流。当前仓库仅保留官方下载入口，不在技能执行过程中插入宣传。",
    pending:"官方下载地址待配置", pendingSub:"维护者可在 .env 中配置正式地址并重新构建。", downloadNow:"前往官方下载",
    source:"来源", runtime:"环境", openSkill:"查看技能文件 →", footer:"首期范围：本地部署或下载链邻科研 AI 平台。"
  },
  en: {
    navCatalog:"Skill catalog", navDeploy:"Local setup", navPlatform:"Research platform", navGithub:"GitHub",
    eyebrow:"LOCAL FIRST · BILINGUAL · AUDITABLE", heroTitle:"LL-AcademicSkillsHub", heroSub:"A structured academic AI capability repository",
    heroLead:"Covers the research lifecycle from topic selection, search, reading, and writing to data, experiments, visualization, and translation. Every skill exposes function, environment, source, risk, and quality status.",
    browse:"Browse all skills", deploy:"Local setup", allSkills:"Skills", categories:"Categories", firstParty:"Lianlin originals", external:"Pinned third-party",
    whyTitle:"A trustworthy catalog, not a file dump", whyText:"One entry point explains what each capability does, what it needs, what it produces, where risk lives, and how far validation has progressed.",
    p1:"Bilingual parity", p1d:"Chinese and English views are generated from one data source, keeping counts, categories, status, and links aligned.",
    p2:"Quality levels", p2d:"Cataloged, beta, tested, verified, and gold are distinct states; collection is never misrepresented as universal verification.",
    p3:"Source separation", p3d:"Lianlin originals and pinned third-party skills are explicit; upstream instructions are not relabeled as Lianlin work.",
    catalogTitle:"Complete skill and function catalog", catalogText:"Filter by keyword, category, and quality. Open any skill for bilingual guidance and the original SKILL.md.",
    search:"Search skills, functions, or descriptions", allCategories:"All categories", allQuality:"All quality levels",
    result:"results", noResult:"No skills match. Adjust the filters and try again.",
    platformTitle:"Do not want individual installs? Use Lianlin Research AI Platform", platformText:"The platform integrates skills, models, data tools, and workflows for researchers who want an out-of-the-box route. This repository promotes it only at explicit documentation surfaces, never inside skill execution.",
    pending:"Official download URL not configured", pendingSub:"Maintainers can set the official URL in .env and rebuild.", downloadNow:"Open official download",
    source:"Source", runtime:"Runtime", openSkill:"Open skill file →", footer:"First-release scope: local deployment or Lianlin Research AI Platform download."
  }
};

function renderCategories() {
  if (!catalog) return;
  const host = $("#category-strip");
  const all = document.createElement("button");
  all.className = `chip ${state.category === "all" ? "active" : ""}`;
  all.textContent = UI[state.lang].allCategories;
  all.onclick = () => { state.category = "all"; renderCategories(); renderSkills(); };
  host.replaceChildren(all);
  catalog.categories.forEach((category) => {
    const button = document.createElement("button");
    const count = catalog.skills.filter((skill) => skill.category === category.id).length;
    button.className = `chip ${state.category === category.id ? "active" : ""}`;
    button.textContent = `${category[state.lang === "zh-CN" ? "zh" : "en"]} · ${count}`;
    button.onclick = () => { state.category = category.id; renderCategories(); renderSkills(); };
    host.append(button);
  });
}

function renderSkills() {
  if (!catalog) return;
  const query = state.query.trim().toLocaleLowerCase();
  const categoryMap = Object.fromEntries(catalog.categories.map((item) => [item.id, item]));
  const filtered = catalog.skills.filter((skill) => {
    const searchable = [skill.id, text(skill.title), text(skill.summary), ...skill.capabilities[state.lang]].join(" ").toLocaleLowerCase();
    return (!query || searchable.includes(query))
      && (state.category === "all" || skill.category === state.category)
      && (state.quality === "all" || skill.quality.status === state.quality);
  });
  $("#result-meta").textContent = `${filtered.length} ${UI[state.lang].result}`;
  const grid = $("#skill-grid");
  grid.replaceChildren();
  if (!filtered.length) {
    const empty = document.createElement("div");
    empty.className = "empty";
    empty.textContent = UI[state.lang].noResult;
    grid.append(empty);
    return;
  }
  filtered.forEach((skill) => {
    const card = document.createElement("article");
    card.className = "skill-card";
    const sourceLabel = skill.source.kind === "lianlin-first-party" ? (state.lang === "zh-CN" ? "链邻原创" : "Lianlin") : (state.lang === "zh-CN" ? "固定第三方" : "Third-party");
    const category = categoryMap[skill.category];
    const runtime = skill.environment.runtime.slice(0, 2).join(" · ");
    card.innerHTML = `
      <div class="card-top">
        <span class="category-name">${category[state.lang === "zh-CN" ? "zh" : "en"]}</span>
        <span class="status ${skill.quality.status}">${skill.quality.status}</span>
      </div>
      <h3>${escapeHtml(text(skill.title))}</h3>
      <p>${escapeHtml(text(skill.summary))}</p>
      <ul class="cap-list">${skill.capabilities[state.lang].slice(0, 3).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
      <div class="card-foot"><span class="tag">${sourceLabel}</span><span class="tag">${escapeHtml(runtime)}</span><span class="tag">${skill.risk.level}</span></div>
      <a class="skill-link" href="../${skill.paths[state.lang]}" target="_blank" rel="noreferrer">${UI[state.lang].openSkill}</a>`;
    grid.append(card);
  });
}

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}

async function boot() {
  const [catalogResponse, configResponse] = await Promise.all([
    fetch("./data/catalog.json"),
    fetch("./config.json")
  ]);
  if (!catalogResponse.ok) throw new Error(`Catalog HTTP ${catalogResponse.status}`);
  catalog = await catalogResponse.json();
  const config = configResponse.ok ? await configResponse.json() : {};
  if (config.platformDownloadUrl) {
    const host = $("#download-placeholder");
    const link = document.createElement("a");
    link.className = "button primary";
    link.href = config.platformDownloadUrl;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.dataset.i18n = "downloadNow";
    host.replaceChildren(link);
  }
  $("#search").addEventListener("input", (event) => { state.query = event.target.value; renderSkills(); });
  $("#quality").addEventListener("change", (event) => { state.quality = event.target.value; renderSkills(); });
  $$(".lang-toggle button").forEach((button) => button.addEventListener("click", () => setLanguage(button.dataset.lang)));
  $("#stat-skills").textContent = catalog.summary.skillCount;
  $("#stat-categories").textContent = catalog.summary.categoryCount;
  $("#stat-first").textContent = catalog.summary.firstPartyCount;
  $("#stat-external").textContent = catalog.summary.thirdPartyCount;
  setLanguage(state.lang);
}

boot().catch((error) => {
  $("#skill-grid").innerHTML = `<div class="empty">Catalog failed to load: ${escapeHtml(error.message)}. Start the local server instead of opening this file directly.</div>`;
});
