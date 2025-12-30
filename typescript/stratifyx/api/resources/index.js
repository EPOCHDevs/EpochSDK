"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.studiesMonteCarlo = exports.studiesAccount = exports.studiesMetrics = exports.studiesPerformance = exports.studiesAnalytics = exports.studiesTables = exports.studiesEvents = exports.studiesExecutions = exports.studiesDefinitions = exports.studies = exports.scriptValidation = exports.studiesEventMarkers = exports.studiesPositions = exports.studiesOrders = exports.documentation = exports.metadata = exports.health = void 0;
exports.health = __importStar(require("./health"));
__exportStar(require("./health/types"), exports);
exports.metadata = __importStar(require("./metadata"));
__exportStar(require("./metadata/types"), exports);
exports.documentation = __importStar(require("./documentation"));
__exportStar(require("./documentation/types"), exports);
exports.studiesOrders = __importStar(require("./studiesOrders"));
__exportStar(require("./studiesOrders/types"), exports);
exports.studiesPositions = __importStar(require("./studiesPositions"));
__exportStar(require("./studiesPositions/types"), exports);
exports.studiesEventMarkers = __importStar(require("./studiesEventMarkers"));
__exportStar(require("./studiesEventMarkers/types"), exports);
exports.scriptValidation = __importStar(require("./scriptValidation"));
exports.studies = __importStar(require("./studies"));
exports.studiesDefinitions = __importStar(require("./studiesDefinitions"));
exports.studiesExecutions = __importStar(require("./studiesExecutions"));
exports.studiesEvents = __importStar(require("./studiesEvents"));
exports.studiesTables = __importStar(require("./studiesTables"));
exports.studiesAnalytics = __importStar(require("./studiesAnalytics"));
exports.studiesPerformance = __importStar(require("./studiesPerformance"));
exports.studiesMetrics = __importStar(require("./studiesMetrics"));
exports.studiesAccount = __importStar(require("./studiesAccount"));
exports.studiesMonteCarlo = __importStar(require("./studiesMonteCarlo"));
__exportStar(require("./metadata/client/requests"), exports);
__exportStar(require("./scriptValidation/client/requests"), exports);
__exportStar(require("./documentation/client/requests"), exports);
__exportStar(require("./studies/client/requests"), exports);
__exportStar(require("./studiesDefinitions/client/requests"), exports);
__exportStar(require("./studiesExecutions/client/requests"), exports);
__exportStar(require("./studiesEvents/client/requests"), exports);
__exportStar(require("./studiesTables/client/requests"), exports);
__exportStar(require("./studiesAnalytics/client/requests"), exports);
__exportStar(require("./studiesPerformance/client/requests"), exports);
__exportStar(require("./studiesMetrics/client/requests"), exports);
__exportStar(require("./studiesAccount/client/requests"), exports);
__exportStar(require("./studiesOrders/client/requests"), exports);
__exportStar(require("./studiesPositions/client/requests"), exports);
__exportStar(require("./studiesEventMarkers/client/requests"), exports);
__exportStar(require("./studiesMonteCarlo/client/requests"), exports);
