import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { createMapping, listMappings } from "../api/client";
import type { AttributeMapping, AttributeMappingInput } from "../api/client";

const emptyMapping: AttributeMappingInput = {
  attribute_code: "",
  human_value: "",
  magento_label: "",
  magento_option_id: "",
  is_active: true,
};

export function MappingPage() {
  const [mappings, setMappings] = useState<AttributeMapping[]>([]);
  const [form, setForm] = useState<AttributeMappingInput>(emptyMapping);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadMappings() {
      try {
        const data = await listMappings();
        if (!cancelled) {
          setMappings(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load mappings");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadMappings();
    return () => {
      cancelled = true;
    };
  }, []);

  function updateForm(field: keyof AttributeMappingInput, value: string | boolean) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      const created = await createMapping(form);
      setMappings((current) => [...current, created]);
      setForm(emptyMapping);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save mapping");
    } finally {
      setSaving(false);
    }
  }

  const canSubmit =
    form.attribute_code.trim() !== "" &&
    form.human_value.trim() !== "" &&
    form.magento_label.trim() !== "" &&
    form.magento_option_id.trim() !== "";

  return (
    <>
      <h2>Magento Attribute Mapping</h2>
      <p className="muted">
        Map staff-friendly values to Magento labels and option IDs before API draft pushes.
      </p>

      <div className="card">
        <h3>Add mapping</h3>
        <form onSubmit={onSubmit}>
          <div className="form-grid">
            <label>
              Attribute code
              <input
                className="input"
                value={form.attribute_code}
                onChange={(event) => updateForm("attribute_code", event.target.value)}
              />
            </label>
            <label>
              Staff value
              <input
                className="input"
                value={form.human_value}
                onChange={(event) => updateForm("human_value", event.target.value)}
              />
            </label>
            <label>
              Magento label
              <input
                className="input"
                value={form.magento_label}
                onChange={(event) => updateForm("magento_label", event.target.value)}
              />
            </label>
            <label>
              Magento option ID
              <input
                className="input"
                value={form.magento_option_id}
                onChange={(event) => updateForm("magento_option_id", event.target.value)}
              />
            </label>
          </div>
          <label className="checkbox-row">
            <input
              type="checkbox"
              checked={form.is_active}
              onChange={(event) => updateForm("is_active", event.target.checked)}
            />
            Active
          </label>
          <button className="primary-button" disabled={!canSubmit || saving}>
            {saving ? "Saving..." : "Save Mapping"}
          </button>
        </form>
        {error && <p className="alert alert-error">{error}</p>}
      </div>

      <div className="card">
        <h3>Current mappings</h3>
        {loading ? (
          <p className="muted">Loading mappings...</p>
        ) : mappings.length === 0 ? (
          <p className="empty-state">No mappings have been configured.</p>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>Attribute</th>
                  <th>Staff value</th>
                  <th>Magento label</th>
                  <th>Option ID</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {mappings.map((mapping) => (
                  <tr key={mapping.id}>
                    <td>{mapping.attribute_code}</td>
                    <td>{mapping.human_value}</td>
                    <td>{mapping.magento_label}</td>
                    <td>{mapping.magento_option_id}</td>
                    <td>
                      <span className="badge">{mapping.is_active ? "active" : "inactive"}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
