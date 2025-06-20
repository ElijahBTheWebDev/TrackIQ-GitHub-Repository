"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Upload, File, X, LoaderCircle } from "lucide-react";

// Define the structure of the audio features
interface AudioFeatures {
  [key: string]: string | number;
}

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null);
  const [features, setFeatures] = useState<AudioFeatures | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (selectedFile: File | null) => {
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
      setFeatures(null);
    }
  };

  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setFeatures(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/process-mp3/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Something went wrong");
      }

      const data = await response.json();
      setFeatures(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="container mx-auto max-w-3xl py-12 px-4">
      <div className="space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            AI Audio Analysis
          </h1>
          <p className="mt-4 text-lg text-muted-foreground">
            Upload your track and let our AI do the rest.
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Upload Your Audio File</CardTitle>
            <CardDescription>
              Drag & drop your audio file here or click to select.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div
              className={`flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg cursor-pointer transition-colors ${
                isDragging ? "border-primary bg-primary/10" : "border-border"
              }`}
              onDragEnter={handleDragEnter}
              onDragOver={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => document.getElementById("file-input")?.click()}
            >
              <Upload className="w-12 h-12 text-muted-foreground" />
              <p className="mt-4 text-muted-foreground">
                Drag & drop or click here
              </p>
              <input
                id="file-input"
                type="file"
                className="hidden"
                onChange={(e) => handleFileChange(e.target.files ? e.target.files[0] : null)}
              />
            </div>

            {file && (
              <div className="flex items-center justify-between p-2 mt-4 border rounded-lg">
                <div className="flex items-center space-x-2">
                  <File className="w-5 h-5" />
                  <span className="text-sm">{file.name}</span>
                </div>
                <Button variant="ghost" size="icon" onClick={() => setFile(null)}>
                  <X className="w-4 h-4" />
                </Button>
              </div>
            )}
            
            <Button onClick={handleUpload} disabled={isLoading || !file} className="w-full">
              {isLoading ? (
                <>
                  <LoaderCircle className="mr-2 h-4 w-4 animate-spin" />
                  Analyzing...
                </>
              ) : "Analyze Audio"}
            </Button>
            {error && (
              <div className="flex items-center p-2 text-sm text-red-500 bg-red-500/10 border border-red-500/20 rounded-lg">
                <X className="w-4 h-4 mr-2" />
                {error}
              </div>
            )}
          </CardContent>
        </Card>

        {features && (
          <Card>
            <CardHeader>
              <CardTitle>Analysis Results</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-6">
                {Object.entries(features).map(([key, value]) => (
                  <div key={key} className="flex flex-col space-y-1">
                    <p className="text-sm font-medium text-muted-foreground">
                      {key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                    </p>
                    <p className="text-xl font-semibold">
                      {typeof value === 'number' ? value.toFixed(2) : value}
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  );
}
