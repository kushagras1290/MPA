export function MappingPage() {
  return (
    <>
      <h2>Magento Attribute Mapping</h2>
      <p className="muted">
        Map staff-friendly values like “Ceylon” or “Oval” to Magento option IDs.
      </p>

      <div className="card">
        <h3>Mapping manager placeholder</h3>
        <p>
          Backend endpoints are present at <code>/api/mappings</code>. Connect this screen to add/edit mappings.
        </p>
      </div>
    </>
  );
}
