function FormRow() {
  return (
    <div className="py-4">
      <span className="flex gap-4">
        <label htmlFor="files">Files: </label>
        <input name="files" type="file" accept=".xlsx, .xls" multiple></input>
      </span>
    </div>
  );
}

export default FormRow;
