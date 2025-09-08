import { API } from "../constants";

import { apiClient } from "@/api/apiClient";
import Blob from "Blob";
import Content from "Content";
import FILES_DELETE from "FILES_DELETE";
import FILES_DOWNLOAD from "FILES_DOWNLOAD";
import FILES_LIST from "FILES_LIST";
import FILES_UPLOAD from "FILES_UPLOAD";
import File from "File";
import FileItem from "FileItem";
import FormData from "FormData";
import Type from "Type";

export type FileItem = {
  id: string;
  name: string;
  size: number;
  contentType?: string;
  createdAt?: string;
};

export async function listFiles(): Promise<FileItem[]> {
  const { data } = await apiClient.get(API.FILES_LIST);
  return data as FileItem[];
}

export async function uploadFile(file: File): Promise<FileItem> {
  const form = new FormData();
  form.append("file", file);
  const { data } = await apiClient.post(API.FILES_UPLOAD, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data as FileItem;
}

export async function downloadFile(fileId: string): Promise<Blob> {
  const { data } = await apiClient.get(API.FILES_DOWNLOAD(fileId), {
    responseType: "blob",
  });
  return data as Blob;
}

export async function deleteFile(fileId: string): Promise<void> {
  await apiClient.delete(API.FILES_DELETE(fileId));
}
