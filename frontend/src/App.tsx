import { useState } from "react";
import { BarChart3, Boxes, FileSpreadsheet, GitBranch, Settings } from "lucide-react";
import { DashboardPage } from "./pages/DashboardPage";
import { UploadPage } from "./pages/UploadPage";
import { ReviewPage } from "./pages/ReviewPage";
import { MappingPage } from "./pages/MappingPage";

type Page = "dashboard" | "upload" | "review" | "mappings";

const nav = [
  { id: "dashboard", label: "Dashboard", icon: BarChart3 },
  { id: "upload", label: "Bulk Upload", icon: FileSpreadsheet },
  { id: "review", label: "Product Review", icon: Boxes },
  { id: "mappings", label: "Mappings", icon: GitBranch }
] as const;

export function App() {
  const [page, setPage] = useState<Page>("dashboard");

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>Magento Product Automation</h1>
        {nav.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              className={`nav-button ${page === item.id ? "active" : ""}`}
              onClick={() => setPage(item.id)}
            >
              <Icon size={16} style={{ marginRight: 8, verticalAlign: "middle" }} />
              {item.label}
            </button>
          );
        })}
        <div style={{ marginTop: 32, color: "#9ca3af", fontSize: 13 }}>
          <Settings size={14} style={{ marginRight: 6, verticalAlign: "middle" }} />
          Draft-first Magento workflow
        </div>
      </aside>
      <main className="main">
        {page === "dashboard" && <DashboardPage />}
        {page === "upload" && <UploadPage />}
        {page === "review" && <ReviewPage />}
        {page === "mappings" && <MappingPage />}
      </main>
    </div>
  );
}
