import { useSnackbar } from "notistack";
import { DragEvent, useCallback, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { startTrainingJob, uploadFiles, watchTraining } from "@/services/training";
import AI from "AI";
import Actions from "Actions";
import Audio from "Audio";
import Bar from "Bar";
import CSV from "CSV";
import ChangeEvent from "ChangeEvent";
import Click from "Click";
import DOCX from "DOCX";
import Enter from "Enter";
import File from "File";
import GIF from "GIF";
import HTMLDivElement from "HTMLDivElement";
import HTMLInputElement from "HTMLInputElement";
import Icon from "Icon";
import Image from "Image";
import Input from "Input";
import JPG from "JPG";
import Learning from "Learning";
import MP3 from "MP3";
import MP4 from "MP4";
import Math from "Math";
import One from "One";
import OneClickDropzone from "OneClickDropzone";
import Overlay from "Overlay";
import PDF from "PDF";
import PNG from "PNG";
import Progress from "Progress";
import Quick from "Quick";
import Reset from "Reset";
import Start from "Start";
import Supported from "Supported";
import TXT from "TXT";
import Training from "../../../pages/Training";
import TrainingProgress from "TrainingProgress";
import Upload from "Upload";
import Video from "Video";
import WAV from "WAV";
import Watch from "Watch";
import XML from "XML";

interface TrainingProgress {
  percent: number;
  status: 'uploading' | 'training' | 'completed' | 'error';
  message?: string;
}

export default function OneClickDropzone() {
  const { t } = useTranslation();
  const { enqueueSnackbar } = useSnackbar();
  const [progress, setProgress] = useState<TrainingProgress>({ percent: 0, status: 'completed' });
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFiles = useCallback(async (files: File[]) => {
    if (files.length === 0) return;

    try {
      setProgress({ percent: 0, status: 'uploading', message: 'Đang tải file...' });
      enqueueSnackbar(`Bắt đầu upload ${files.length} file(s)`, { variant: 'info' });

      // Upload files
      const uploadResult = await uploadFiles(files);
      setProgress({ percent: 25, status: 'uploading', message: 'Upload hoàn thành' });

      // Start training job
      setProgress({ percent: 30, status: 'training', message: 'Khởi tạo huấn luyện...' });
      const trainingJob = await startTrainingJob(uploadResult.jobId);
      
      enqueueSnackbar('Đã khởi động huấn luyện AI', { variant: 'success' });

      // Watch training progress
      let lastPercent = 30;
      for await (const progressUpdate of watchTraining(trainingJob.id)) {
        const newPercent = Math.max(lastPercent, 30 + (progressUpdate.progress * 0.7)); // 30-100%
        setProgress({ 
          percent: newPercent, 
          status: 'training',
          message: `Đang huấn luyện... ${Math.round(progressUpdate.progress)}%`
        });
        lastPercent = newPercent;

        if (progressUpdate.progress >= 100) {
          setProgress({ percent: 100, status: 'completed', message: 'Hoàn thành!' });
          enqueueSnackbar('Huấn luyện AI hoàn thành thành công!', { variant: 'success' });
          break;
        }
      }

    } catch (error) {
      console.error('Training error:', error);
      setProgress({ percent: 0, status: 'error', message: 'Có lỗi xảy ra' });
      enqueueSnackbar(`Lỗi: ${error}`, { variant: 'error' });
    }
  }, [enqueueSnackbar]);

  const onDrop = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  }, [handleFiles]);

  const onDragOver = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const onDragLeave = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const onFileSelect = useCallback(() => {
    fileInputRef.current?.click();
  }, []);

  const onFileInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    handleFiles(files);
    // Reset input để có thể chọn lại cùng file
    e.target.value = '';
  }, [handleFiles]);

  const getStatusColor = () => {
    switch (progress.status) {
      case 'uploading': return 'bg-blue-500';
      case 'training': return 'bg-yellow-500';
      case 'completed': return 'bg-green-500';
      case 'error': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusIcon = () => {
    switch (progress.status) {
      case 'uploading': return '📤';
      case 'training': return '🧠';
      case 'completed': return '✅';
      case 'error': return '❌';
      default: return '📁';
    }
  };

  const isProcessing = progress.status === 'uploading' || progress.status === 'training';

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="mb-6 text-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          One-Click Learning
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Kéo thả file hoặc click để bắt đầu huấn luyện AI ngay lập tức
        </p>
      </div>

      <div
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        onClick={onFileSelect}
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 cursor-pointer
          ${isDragOver 
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
          }
          ${isProcessing ? 'opacity-75 cursor-not-allowed' : ''}
        `}
        role="button"
        aria-label="Kéo thả file để huấn luyện AI"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onFileSelect();
          }
        }}
      >
        {/* Icon và text */}
        <div className="mb-4">
          <div className="text-6xl mb-4">
            {isProcessing ? getStatusIcon() : '🎯'}
          </div>
          <div className="space-y-2">
            <p className="text-lg font-medium text-gray-900 dark:text-white">
              {isProcessing 
                ? progress.message || 'Đang xử lý...'
                : 'Kéo thả file vào đây'
              }
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {isProcessing 
                ? `${Math.round(progress.percent)}% hoàn thành`
                : 'Hỗ trợ: PDF, DOCX, TXT, JSON, CSV, Image, Audio, Video'
              }
            </p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mt-6">
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
            <div 
              className={`h-full transition-all duration-300 ease-out ${getStatusColor()}`}
              style={{ width: `${progress.percent}%` }}
            />
          </div>
        </div>

        {/* File Input (hidden) */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          className="hidden"
          onChange={onFileInputChange}
          accept=".pdf,.doc,.docx,.txt,.json,.csv,.png,.jpg,.jpeg,.mp3,.wav,.mp4,.avi"
          disabled={isProcessing}
        />

        {/* Overlay khi processing */}
        {isProcessing && (
          <div className="absolute inset-0 rounded-xl bg-white/50 dark:bg-black/50 flex items-center justify-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="mt-6 flex justify-center space-x-4">
        <button
          onClick={onFileSelect}
          disabled={isProcessing}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          📁 Chọn File
        </button>
        {progress.status === 'completed' && (
          <button
            onClick={() => setProgress({ percent: 0, status: 'completed' })}
            className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
          >
            🔄 Làm mới
          </button>
        )}
      </div>

      {/* Supported formats */}
      <div className="mt-6 text-center">
        <details className="text-sm text-gray-500 dark:text-gray-400">
          <summary className="cursor-pointer hover:text-gray-700 dark:hover:text-gray-300">
            Định dạng file được hỗ trợ
          </summary>
          <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
            <div>📄 Văn bản: PDF, DOCX, TXT</div>
            <div>📊 Dữ liệu: JSON, CSV, XML</div>
            <div>🖼️ Hình ảnh: PNG, JPG, GIF</div>
            <div>🎵 Audio/Video: MP3, WAV, MP4</div>
          </div>
        </details>
      </div>
    </div>
  );
}
