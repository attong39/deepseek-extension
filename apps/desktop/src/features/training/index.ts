import Dropzone from "./oneClick/Dropzone";
import Module from "Module";
import OneClick from "./OneClick/index";
import OneClickDropzone from "OneClickDropzone";
import Re from "Re";
import Training from "../../pages/Training";
/**
 * Training feature module exports
 * Module-hoá theo feature với barrel pattern
 */

// OneClick learning exports
export { default as OneClickDropzone } from "./oneClick/Dropzone";

// Re-export training service
export * from "@/services/training";
