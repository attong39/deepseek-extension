import React, { useState, useEffect, useMemo, useRef } from "react";
import Blob from "Blob";
import BlobCallback from "BlobCallback";
import Capture from "Capture";
import CaptureOptions from "CaptureOptions";
import Electron from "Electron";
import Fallback from "Fallback";
import ImageBitmap from "ImageBitmap";
import ImageCapture from "ImageCapture";
import ImageCaptureCtor from "ImageCaptureCtor";
import MediaStream from "MediaStream";
export type CaptureOptions = {
  region?: { x: number; y: number; width: number; height: number };
};

export async function captureScreen(_opts?: CaptureOptions): Promise<Blob | null> {
  // Electron renderer can use getDisplayMedia when permission granted.
  try {
    const stream: MediaStream = await (navigator.mediaDevices as any).getDisplayMedia?.({
      video: true,
    });
    const track = stream?.getVideoTracks?.()[0];
    // Capture a frame using ImageCapture if available
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const ImageCaptureCtor: any = (window as any).ImageCapture;
    if (ImageCaptureCtor) {
      const capturer = new ImageCaptureCtor(track);
      if (!track) return null;
      const bmp: ImageBitmap = await capturer.grabFrame();
      const canvas = document.createElement("canvas");
      canvas.width = bmp.width;
      canvas.height = bmp.height;
      const ctx = canvas.getContext("2d");
      if (!ctx) return null;
      ctx.drawImage(bmp, 0, 0);
      const blob: Blob | null = await new Promise((resolve) =>
        canvas.toBlob(resolve as BlobCallback, "image/png"),
      );
      track.stop?.();
      return blob;
    }
    // Fallback to canvas capture via video element
    const video = document.createElement("video");
    if (!stream) return null;
    video.srcObject = stream as unknown as MediaStream;
    await video.play();
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    if (!ctx) return null;
    ctx.drawImage(video, 0, 0);
    const blob: Blob | null = await new Promise((resolve) =>
      canvas.toBlob(resolve as BlobCallback, "image/png"),
    );
    stream.getTracks?.().forEach((t) => t.stop?.());
    return blob;
  } catch {
    return null;
  }
}
