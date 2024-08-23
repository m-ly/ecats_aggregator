import { useEffect, useState } from "react";
import FormRow from "./FormRow";

function Form() {
  const [uploadedFiles, setupLoadedFiles] = useState([]);
  const [script, setScript] = useState("status");
  const [downloadUrl, setDownLoadUrl] = useState("");

  function handleFileEvent(e) {
    const chosenFiles = Array.prototype.slice.call(e.target.files);
    setupLoadedFiles(chosenFiles);
  }

  async function handleUpload(e) {
    e.preventDefault();

    const formData = new FormData();

    formData.append("script", script);

    uploadedFiles.forEach((file, index) => {
      formData.append(`file_${index}`, file);
    });

    try {
      let response = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      let res = await response.json();

      if (res.status === 0) {
        alert("Error Uploading file");
      } else {
        console.log("Files uploaded successfully");
        setDownLoadUrl(res.download_url);
        if (downloadUrl) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = downloadUrl.split("/").pop();
          document.body.appendChild(a);
          a.click();
          a.remove();
          window.URL.revokeObjectURL(url);
          console.log("Download initiated successfully");
        }
      }
    } catch (error) {
      console.error("Error uploading files:", error);
    }
  }

  useEffect(() => {
    if (downloadUrl) {
      handleDownloadFile();
    }
  }, [downloadUrl]);

  async function handleDownloadFile() {
    try {
      console.log("attempting get function");
      let response = await fetch(downloadUrl, {
        method: "GET",
      });
      if (response.ok) {
        console.log("success!");
        console.log(response);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = downloadUrl.split("/").pop();
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        console.log("Download initiated successfully");
      } else {
        console.error("Error downloading the file");
      }
    } catch (error) {
      console.error("Error uploading files:", error);
    }
  }

  return (
    <>
      <form
        className="flex flex-col justify-center border-2 border-stone-500 py-4 px-16 content-center"
        onSubmit={handleUpload}
        encType="multipart/form-data"
      >
        <fieldset className="flex  gap-4">
          <label>
            <input
              type="radio"
              value="status"
              name="command"
              defaultChecked={true}
              onChange={() => setScript("status")}
            />
            Status Report
          </label>
          <label>
            <input
              type="radio"
              value="ready"
              name="command"
              onChange={() => setScript("ready")}
            />
            Ready Report
          </label>
        </fieldset>

        <div className="py-4">
          <span className="flex gap-4">
            <label htmlFor="files">Files: </label>

            {uploadedFiles.length >= 1 ? (
              <ul>
                {console.log(uploadedFiles)}
                {uploadedFiles.map((file) => (
                  <li key={Math.random()}>{file.name}</li>
                ))}
              </ul>
            ) : (
              <input
                name="files"
                type="file"
                onChange={handleFileEvent}
                accept=".xls"
                multiple
              ></input>
            )}
          </span>
        </div>

        <button
          className="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-4 px-4 rounded"
          type="submit"
        >
          Upload and Aggregate
        </button>
      </form>

      <div className="mt-10 border-2 border-red-500 text-xl p-8">
        <h2>Usage Instructions:</h2>
        <ol className="list-decimal text-sm">
          <li>All Input items must be of an xls format</li>
          <li>
            Each separate file must include an abbreviation of the the role that
            is being tracked. The only acceptable role names are as follows:
            <ul className="ml-8 list-disc">
              <li>Channel 1: ch1</li>
              <li>Channel 2: ch2</li>
              <li>Fire: fire</li>
              <li>Phones: phones</li>
              <li>Training: training</li>
              <li className="ml-12 italic">
                Example file name: &apos;ch1_we_07022024&apos;
              </li>
            </ul>
          </li>
        </ol>
      </div>
    </>
  );
}

export default Form;
