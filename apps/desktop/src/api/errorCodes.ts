import AUTH_001 from "AUTH_001";
import AUTH_002 from "AUTH_002";
import AUTH_003 from "AUTH_003";
import AUTH_004 from "AUTH_004";
import AUTH_005 from "AUTH_005";
import AUTH_006 from "AUTH_006";
import AUTH_007 from "AUTH_007";
import AUTH_EXPIRED from "AUTH_EXPIRED";
import AUTH_INVALID from "AUTH_INVALID";
import AUTH_XXX from "AUTH_XXX";
import AgentCreationError from "AgentCreationError";
import AgentDeploymentError from "AgentDeploymentError";
import AgentNotFoundError from "AgentNotFoundError";
import Auth from "./Auth";
import AuthenticationError from "AuthenticationError";
import AuthorizationError from "AuthorizationError";
import BIZ_001 from "BIZ_001";
import BIZ_002 from "BIZ_002";
import BIZ_003 from "BIZ_003";
import BIZ_004 from "BIZ_004";
import BIZ_005 from "BIZ_005";
import BIZ_006 from "BIZ_006";
import BIZ_007 from "BIZ_007";
import BIZ_008 from "BIZ_008";
import BIZ_009 from "BIZ_009";
import BIZ_010 from "BIZ_010";
import BIZ_011 from "BIZ_011";
import BIZ_012 from "BIZ_012";
import BIZ_013 from "BIZ_013";
import BIZ_014 from "BIZ_014";
import BIZ_015 from "BIZ_015";
import BIZ_016 from "BIZ_016";
import BIZ_XXX from "BIZ_XXX";
import BackupError from "BackupError";
import Backward from "Backward";
import Business from "Business";
import BusinessRuleViolationError from "BusinessRuleViolationError";
import CacheConnectionError from "CacheConnectionError";
import CacheError from "CacheError";
import ChatSessionError from "ChatSessionError";
import ConnectionPoolExhaustedError from "ConnectionPoolExhaustedError";
import Data from "Data";
import DataIntegrityError from "DataIntegrityError";
import DatabaseConnectionError from "DatabaseConnectionError";
import Deadlock from "Deadlock";
import DeadlockError from "DeadlockError";
import DuplicateRecordError from "DuplicateRecordError";
import ERROR_MESSAGES from "ERROR_MESSAGES";
import EmbeddingDimensionError from "EmbeddingDimensionError";
import EntityNotFoundError from "EntityNotFoundError";
import ExternalServiceError from "ExternalServiceError";
import Fallback from "Fallback";
import ForeignKeyViolationError from "ForeignKeyViolationError";
import Giao from "Giao";
import HTTP from "HTTP";
import InvalidCredentialsError from "InvalidCredentialsError";
import InvalidTokenError from "InvalidTokenError";
import JWTTokenError from "JWTTokenError";
import Keep from "Keep";
import MFA from "MFA";
import MFARequiredError from "MFARequiredError";
import Map from "Map";
import MemoryOperationError from "MemoryOperationError";
import MessageProcessingError from "MessageProcessingError";
import MigrationError from "MigrationError";
import ModelLoadError from "ModelLoadError";
import Other from "Other";
import PermissionDeniedError from "PermissionDeniedError";
import PlanningError from "PlanningError";
import Pool from "Pool";
import QueryExecutionError from "QueryExecutionError";
import QueryTimeoutError from "QueryTimeoutError";
import RATE_LIMITED from "RATE_LIMITED";
import REPO_001 from "REPO_001";
import REPO_002 from "REPO_002";
import REPO_003 from "REPO_003";
import REPO_004 from "REPO_004";
import REPO_005 from "REPO_005";
import REPO_006 from "REPO_006";
import REPO_007 from "REPO_007";
import REPO_008 from "REPO_008";
import REPO_009 from "REPO_009";
import REPO_010 from "REPO_010";
import REPO_011 from "REPO_011";
import REPO_012 from "REPO_012";
import REPO_013 from "REPO_013";
import REPO_014 from "REPO_014";
import REPO_015 from "REPO_015";
import REPO_016 from "REPO_016";
import REPO_017 from "REPO_017";
import REPO_XXX from "REPO_XXX";
import RateLimitExceededError from "RateLimitExceededError";
import Record from "Record";
import RecordNotFoundError from "RecordNotFoundError";
import Repository from "Repository";
import ResourceLimitExceededError from "ResourceLimitExceededError";
import Sai from "Sai";
import SessionExpiredError from "SessionExpiredError";
import Token from "Token";
import TrainingError from "TrainingError";
import TransactionError from "TransactionError";
import Truy from "Truy";
import Try from "Try";
import UNKNOWN from "UNKNOWN";
import VALIDATION_FAILED from "VALIDATION_FAILED";
import ValidationError from "ValidationError";
import VectorDatabaseError from "VectorDatabaseError";
import VectorEmbeddingError from "VectorEmbeddingError";
import Vi from "Vi";
import WorkflowExecutionError from "WorkflowExecutionError";
// Map error codes to user-friendly messages. Keep in sync with server exceptions:
// - core/exceptions/auth_exceptions.py (AUTH_XXX)
// - core/exceptions/business_exceptions.py (BIZ_XXX)
// - core/exceptions/repository_exceptions.py (REPO_XXX)
export const ERROR_MESSAGES: Record<string, string> = {
  // ---- Backward-compat aliases ----
  AUTH_INVALID: "Thông tin đăng nhập không hợp lệ.", // → AUTH_001
  AUTH_EXPIRED: "Phiên đăng nhập đã hết hạn.", // → AUTH_005
  RATE_LIMITED: "Bạn thao tác quá nhanh, vui lòng thử lại sau.", // → AUTH_007
  VALIDATION_FAILED: "Dữ liệu không hợp lệ.", // → BIZ_012 / REPO_017

  // ---- Auth errors (AUTH_XXX) ----
  AUTH_001: "Thông tin đăng nhập không hợp lệ.", // AuthenticationError / InvalidCredentialsError
  AUTH_002: "Bạn không có đủ quyền để thực hiện thao tác này.", // AuthorizationError
  AUTH_003: "Token không hợp lệ hoặc đã hết hạn.", // JWTTokenError / InvalidTokenError
  AUTH_004: "Yêu cầu xác thực đa yếu tố (MFA).", // MFARequiredError
  AUTH_005: "Phiên làm việc đã hết hạn.", // SessionExpiredError
  AUTH_006: "Truy cập bị từ chối cho tài nguyên yêu cầu.", // PermissionDeniedError
  AUTH_007: "Bạn thao tác quá nhanh, vui lòng thử lại sau.", // RateLimitExceededError
  AUTH_EXPIRED: "Phiên đăng nhập đã hết hạn.", //
  AUTH_INVALID: "Thông tin đăng nhập không hợp lệ.", //

  // ---- Business errors (BIZ_XXX) ----
  BIZ_001: "Không tìm thấy agent.", // AgentNotFoundError
  BIZ_002: "Tạo agent thất bại.", // AgentCreationError
  BIZ_003: "Triển khai agent thất bại.", // AgentDeploymentError
  BIZ_004: "Lỗi phiên chat.", // ChatSessionError
  BIZ_005: "Xử lý tin nhắn thất bại.", // MessageProcessingError
  BIZ_006: "Lỗi thao tác bộ nhớ.", // MemoryOperationError
  BIZ_007: "Lỗi vector embedding.", // VectorEmbeddingError
  BIZ_008: "Lỗi lập kế hoạch.", // PlanningError
  BIZ_009: "Lỗi thực thi quy trình.", // WorkflowExecutionError
  BIZ_010: "Lỗi huấn luyện mô hình.", // TrainingError
  BIZ_011: "Lỗi tải mô hình.", // ModelLoadError
  BIZ_012: "Dữ liệu không hợp lệ.", // ValidationError (business)
  BIZ_013: "Vi phạm luật nghiệp vụ.", // BusinessRuleViolationError
  BIZ_014: "Vượt giới hạn tài nguyên.", // ResourceLimitExceededError
  BIZ_015: "Dịch vụ bên ngoài gặp lỗi.", // ExternalServiceError
  BIZ_016: "Không tìm thấy thực thể.", // EntityNotFoundError

  // ---- Repository/Data errors (REPO_XXX) ----
  REPO_001: "Kết nối cơ sở dữ liệu thất bại.", // DatabaseConnectionError
  REPO_002: "Pool kết nối cơ sở dữ liệu bị cạn kiệt.", // ConnectionPoolExhaustedError
  REPO_003: "Vi phạm toàn vẹn dữ liệu.", // DataIntegrityError
  REPO_004: "Vi phạm khóa ngoại.", // ForeignKeyViolationError
  REPO_005: "Không tìm thấy bản ghi.", // RecordNotFoundError
  REPO_006: "Bản ghi trùng lặp.", // DuplicateRecordError
  REPO_007: "Thực thi truy vấn thất bại.", // QueryExecutionError
  REPO_008: "Truy vấn quá thời gian.", // QueryTimeoutError
  REPO_009: "Giao dịch cơ sở dữ liệu lỗi.", // TransactionError
  REPO_010: "Deadlock cơ sở dữ liệu.", // DeadlockError
  REPO_011: "Lỗi cơ sở dữ liệu vector.", // VectorDatabaseError
  REPO_012: "Sai kích thước embedding.", // EmbeddingDimensionError
  REPO_013: "Lỗi bộ nhớ đệm (cache).", // CacheError
  REPO_014: "Kết nối cache thất bại.", // CacheConnectionError
  REPO_015: "Lỗi migration cơ sở dữ liệu.", // MigrationError
  REPO_016: "Lỗi sao lưu dữ liệu.", // BackupError
  REPO_017: "Dữ liệu không hợp lệ.", // ValidationError (repository)

  // ---- Other errors ----
  RATE_LIMITED: "Bạn thao tác quá nhanh, vui lòng thử lại sau.",
  UNKNOWN: "Đã xảy ra lỗi không xác định.",
  VALIDATION_FAILED: "Dữ liệu không hợp lệ.",

  // ---- Fallback ----
  UNKNOWN: "Đã xảy ra lỗi không xác định.",
};

export function messageFor(code?: string, fallback?: string): string {
  const defaultUnknown = "Đã xảy ra lỗi không xác định.";
  const fb = (typeof fallback === "string" ? fallback : ERROR_MESSAGES.UNKNOWN) ?? defaultUnknown;
  if (!code) return fb;
  // Backward-compat alias mapping
  const alias: Record<string, string> = {
    AUTH_INVALID: "AUTH_001",
    AUTH_EXPIRED: "AUTH_005",
    RATE_LIMITED: "AUTH_007",
    VALIDATION_FAILED: "BIZ_012",
  };
  const normalized: string = alias[code] ?? code;
  const byNormalized = ERROR_MESSAGES[normalized];
  if (byNormalized != null) return byNormalized;
  const byCode = ERROR_MESSAGES[code];
  return byCode ?? fb;
}

// Try to extract error code from common HTTP client error shapes
export function extractErrorCode(err: unknown): string | undefined {
  const e: any = err as any;
  // axios-like: e.response.data.error_code or e.response.data.code
  const fromResponse = e?.response?.data?.error_code || e?.response?.data?.code;
  if (typeof fromResponse === "string") return fromResponse;
  // direct shape
  if (typeof e?.error_code === "string") return e.error_code;
  if (typeof e?.code === "string") return e.code;
  // map from HTTP status if available (best-effort)
  const status = e?.response?.status;
  if (status === 401) return "AUTH_003"; // invalid/expired token
  if (status === 403) return "AUTH_002"; // forbidden
  if (status === 404) return "BIZ_016"; // entity not found (generic)
  if (status === 429) return "AUTH_007"; // rate limited
  if (status === 422) return "BIZ_012"; // validation error
  return undefined;
}

export function messageFromError(err: unknown, fallback?: string): string {
  const code = extractErrorCode(err);
  return messageFor(code, fallback);
}
