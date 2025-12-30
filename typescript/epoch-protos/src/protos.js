/*eslint-disable block-scoped-var, id-length, no-control-regex, no-magic-numbers, no-prototype-builtins, no-redeclare, no-shadow, no-var, sort-vars*/
"use strict";

import $protobuf from "protobufjs/minimal";

// Common aliases
const $Reader = $protobuf.Reader, $Writer = $protobuf.Writer, $util = $protobuf.util;

// Exported root namespace
const $root = $protobuf.roots["default"] || ($protobuf.roots["default"] = {});

export const epoch_proto = $root.epoch_proto = (() => {

    /**
     * Namespace epoch_proto.
     * @exports epoch_proto
     * @namespace
     */
    const epoch_proto = {};

    /**
     * EpochFolioDashboardWidget enum.
     * @name epoch_proto.EpochFolioDashboardWidget
     * @enum {number}
     * @property {number} WidgetUnspecified=0 WidgetUnspecified value
     * @property {number} WidgetCard=1 WidgetCard value
     * @property {number} WidgetLines=2 WidgetLines value
     * @property {number} WidgetBar=3 WidgetBar value
     * @property {number} WidgetDataTable=4 WidgetDataTable value
     * @property {number} WidgetXRange=5 WidgetXRange value
     * @property {number} WidgetHistogram=6 WidgetHistogram value
     * @property {number} WidgetPie=7 WidgetPie value
     * @property {number} WidgetHeatMap=8 WidgetHeatMap value
     * @property {number} WidgetBoxPlot=9 WidgetBoxPlot value
     * @property {number} WidgetArea=10 WidgetArea value
     * @property {number} WidgetColumn=11 WidgetColumn value
     * @property {number} WidgetScatter=12 WidgetScatter value
     * @property {number} WidgetWaterfall=13 WidgetWaterfall value
     * @property {number} WidgetSpline=14 WidgetSpline value
     * @property {number} WidgetBubble=15 WidgetBubble value
     * @property {number} WidgetTreemap=16 WidgetTreemap value
     * @property {number} WidgetSankey=17 WidgetSankey value
     * @property {number} WidgetAreaRange=18 WidgetAreaRange value
     * @property {number} WidgetGauge=19 WidgetGauge value
     * @property {number} WidgetBullet=20 WidgetBullet value
     * @property {number} WidgetTimeline=21 WidgetTimeline value
     * @property {number} WidgetErrorBar=22 WidgetErrorBar value
     * @property {number} WidgetBellCurve=23 WidgetBellCurve value
     * @property {number} WidgetNumericErrorBar=24 WidgetNumericErrorBar value
     */
    epoch_proto.EpochFolioDashboardWidget = (function() {
        const valuesById = {}, values = Object.create(valuesById);
        values[valuesById[0] = "WidgetUnspecified"] = 0;
        values[valuesById[1] = "WidgetCard"] = 1;
        values[valuesById[2] = "WidgetLines"] = 2;
        values[valuesById[3] = "WidgetBar"] = 3;
        values[valuesById[4] = "WidgetDataTable"] = 4;
        values[valuesById[5] = "WidgetXRange"] = 5;
        values[valuesById[6] = "WidgetHistogram"] = 6;
        values[valuesById[7] = "WidgetPie"] = 7;
        values[valuesById[8] = "WidgetHeatMap"] = 8;
        values[valuesById[9] = "WidgetBoxPlot"] = 9;
        values[valuesById[10] = "WidgetArea"] = 10;
        values[valuesById[11] = "WidgetColumn"] = 11;
        values[valuesById[12] = "WidgetScatter"] = 12;
        values[valuesById[13] = "WidgetWaterfall"] = 13;
        values[valuesById[14] = "WidgetSpline"] = 14;
        values[valuesById[15] = "WidgetBubble"] = 15;
        values[valuesById[16] = "WidgetTreemap"] = 16;
        values[valuesById[17] = "WidgetSankey"] = 17;
        values[valuesById[18] = "WidgetAreaRange"] = 18;
        values[valuesById[19] = "WidgetGauge"] = 19;
        values[valuesById[20] = "WidgetBullet"] = 20;
        values[valuesById[21] = "WidgetTimeline"] = 21;
        values[valuesById[22] = "WidgetErrorBar"] = 22;
        values[valuesById[23] = "WidgetBellCurve"] = 23;
        values[valuesById[24] = "WidgetNumericErrorBar"] = 24;
        return values;
    })();

    /**
     * EpochFolioType enum.
     * @name epoch_proto.EpochFolioType
     * @enum {number}
     * @property {number} TypeUnspecified=0 TypeUnspecified value
     * @property {number} TypeString=1 TypeString value
     * @property {number} TypeInteger=2 TypeInteger value
     * @property {number} TypeDecimal=3 TypeDecimal value
     * @property {number} TypePercent=4 TypePercent value
     * @property {number} TypeBoolean=5 TypeBoolean value
     * @property {number} TypeDateTime=6 TypeDateTime value
     * @property {number} TypeDate=7 TypeDate value
     * @property {number} TypeDayDuration=8 TypeDayDuration value
     * @property {number} TypeMonetary=9 TypeMonetary value
     * @property {number} TypeDuration=10 TypeDuration value
     */
    epoch_proto.EpochFolioType = (function() {
        const valuesById = {}, values = Object.create(valuesById);
        values[valuesById[0] = "TypeUnspecified"] = 0;
        values[valuesById[1] = "TypeString"] = 1;
        values[valuesById[2] = "TypeInteger"] = 2;
        values[valuesById[3] = "TypeDecimal"] = 3;
        values[valuesById[4] = "TypePercent"] = 4;
        values[valuesById[5] = "TypeBoolean"] = 5;
        values[valuesById[6] = "TypeDateTime"] = 6;
        values[valuesById[7] = "TypeDate"] = 7;
        values[valuesById[8] = "TypeDayDuration"] = 8;
        values[valuesById[9] = "TypeMonetary"] = 9;
        values[valuesById[10] = "TypeDuration"] = 10;
        return values;
    })();

    /**
     * NullValue enum.
     * @name epoch_proto.NullValue
     * @enum {number}
     * @property {number} NULL_VALUE=0 NULL_VALUE value
     */
    epoch_proto.NullValue = (function() {
        const valuesById = {}, values = Object.create(valuesById);
        values[valuesById[0] = "NULL_VALUE"] = 0;
        return values;
    })();

    epoch_proto.Scalar = (function() {

        /**
         * Properties of a Scalar.
         * @memberof epoch_proto
         * @interface IScalar
         * @property {string|null} [stringValue] Scalar stringValue
         * @property {number|Long|null} [integerValue] Scalar integerValue
         * @property {number|null} [decimalValue] Scalar decimalValue
         * @property {number|null} [percentValue] Scalar percentValue
         * @property {boolean|null} [booleanValue] Scalar booleanValue
         * @property {number|Long|null} [timestampMs] Scalar timestampMs
         * @property {number|Long|null} [dateValue] Scalar dateValue
         * @property {number|null} [dayDuration] Scalar dayDuration
         * @property {number|null} [monetaryValue] Scalar monetaryValue
         * @property {number|Long|null} [durationMs] Scalar durationMs
         * @property {epoch_proto.NullValue|null} [nullValue] Scalar nullValue
         */

        /**
         * Constructs a new Scalar.
         * @memberof epoch_proto
         * @classdesc Represents a Scalar.
         * @implements IScalar
         * @constructor
         * @param {epoch_proto.IScalar=} [properties] Properties to set
         */
        function Scalar(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Scalar stringValue.
         * @member {string|null|undefined} stringValue
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.stringValue = null;

        /**
         * Scalar integerValue.
         * @member {number|Long|null|undefined} integerValue
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.integerValue = null;

        /**
         * Scalar decimalValue.
         * @member {number|null|undefined} decimalValue
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.decimalValue = null;

        /**
         * Scalar percentValue.
         * @member {number|null|undefined} percentValue
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.percentValue = null;

        /**
         * Scalar booleanValue.
         * @member {boolean|null|undefined} booleanValue
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.booleanValue = null;

        /**
         * Scalar timestampMs.
         * @member {number|Long|null|undefined} timestampMs
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.timestampMs = null;

        /**
         * Scalar dateValue.
         * @member {number|Long|null|undefined} dateValue
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.dateValue = null;

        /**
         * Scalar dayDuration.
         * @member {number|null|undefined} dayDuration
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.dayDuration = null;

        /**
         * Scalar monetaryValue.
         * @member {number|null|undefined} monetaryValue
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.monetaryValue = null;

        /**
         * Scalar durationMs.
         * @member {number|Long|null|undefined} durationMs
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.durationMs = null;

        /**
         * Scalar nullValue.
         * @member {epoch_proto.NullValue|null|undefined} nullValue
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Scalar.prototype.nullValue = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        /**
         * Scalar value.
         * @member {"stringValue"|"integerValue"|"decimalValue"|"percentValue"|"booleanValue"|"timestampMs"|"dateValue"|"dayDuration"|"monetaryValue"|"durationMs"|"nullValue"|undefined} value
         * @memberof epoch_proto.Scalar
         * @instance
         */
        Object.defineProperty(Scalar.prototype, "value", {
            get: $util.oneOfGetter($oneOfFields = ["stringValue", "integerValue", "decimalValue", "percentValue", "booleanValue", "timestampMs", "dateValue", "dayDuration", "monetaryValue", "durationMs", "nullValue"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new Scalar instance using the specified properties.
         * @function create
         * @memberof epoch_proto.Scalar
         * @static
         * @param {epoch_proto.IScalar=} [properties] Properties to set
         * @returns {epoch_proto.Scalar} Scalar instance
         */
        Scalar.create = function create(properties) {
            return new Scalar(properties);
        };

        /**
         * Encodes the specified Scalar message. Does not implicitly {@link epoch_proto.Scalar.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.Scalar
         * @static
         * @param {epoch_proto.IScalar} message Scalar message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Scalar.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.stringValue != null && Object.hasOwnProperty.call(message, "stringValue"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.stringValue);
            if (message.integerValue != null && Object.hasOwnProperty.call(message, "integerValue"))
                writer.uint32(/* id 2, wireType 0 =*/16).int64(message.integerValue);
            if (message.decimalValue != null && Object.hasOwnProperty.call(message, "decimalValue"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.decimalValue);
            if (message.percentValue != null && Object.hasOwnProperty.call(message, "percentValue"))
                writer.uint32(/* id 4, wireType 1 =*/33).double(message.percentValue);
            if (message.booleanValue != null && Object.hasOwnProperty.call(message, "booleanValue"))
                writer.uint32(/* id 5, wireType 0 =*/40).bool(message.booleanValue);
            if (message.timestampMs != null && Object.hasOwnProperty.call(message, "timestampMs"))
                writer.uint32(/* id 6, wireType 0 =*/48).int64(message.timestampMs);
            if (message.dateValue != null && Object.hasOwnProperty.call(message, "dateValue"))
                writer.uint32(/* id 7, wireType 0 =*/56).int64(message.dateValue);
            if (message.dayDuration != null && Object.hasOwnProperty.call(message, "dayDuration"))
                writer.uint32(/* id 8, wireType 0 =*/64).int32(message.dayDuration);
            if (message.monetaryValue != null && Object.hasOwnProperty.call(message, "monetaryValue"))
                writer.uint32(/* id 9, wireType 1 =*/73).double(message.monetaryValue);
            if (message.durationMs != null && Object.hasOwnProperty.call(message, "durationMs"))
                writer.uint32(/* id 10, wireType 0 =*/80).int64(message.durationMs);
            if (message.nullValue != null && Object.hasOwnProperty.call(message, "nullValue"))
                writer.uint32(/* id 11, wireType 0 =*/88).int32(message.nullValue);
            return writer;
        };

        /**
         * Encodes the specified Scalar message, length delimited. Does not implicitly {@link epoch_proto.Scalar.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.Scalar
         * @static
         * @param {epoch_proto.IScalar} message Scalar message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Scalar.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a Scalar message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.Scalar
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.Scalar} Scalar
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Scalar.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.Scalar();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.stringValue = reader.string();
                        break;
                    }
                case 2: {
                        message.integerValue = reader.int64();
                        break;
                    }
                case 3: {
                        message.decimalValue = reader.double();
                        break;
                    }
                case 4: {
                        message.percentValue = reader.double();
                        break;
                    }
                case 5: {
                        message.booleanValue = reader.bool();
                        break;
                    }
                case 6: {
                        message.timestampMs = reader.int64();
                        break;
                    }
                case 7: {
                        message.dateValue = reader.int64();
                        break;
                    }
                case 8: {
                        message.dayDuration = reader.int32();
                        break;
                    }
                case 9: {
                        message.monetaryValue = reader.double();
                        break;
                    }
                case 10: {
                        message.durationMs = reader.int64();
                        break;
                    }
                case 11: {
                        message.nullValue = reader.int32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a Scalar message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.Scalar
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.Scalar} Scalar
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Scalar.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a Scalar message.
         * @function verify
         * @memberof epoch_proto.Scalar
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Scalar.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.stringValue != null && message.hasOwnProperty("stringValue")) {
                properties.value = 1;
                if (!$util.isString(message.stringValue))
                    return "stringValue: string expected";
            }
            if (message.integerValue != null && message.hasOwnProperty("integerValue")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                if (!$util.isInteger(message.integerValue) && !(message.integerValue && $util.isInteger(message.integerValue.low) && $util.isInteger(message.integerValue.high)))
                    return "integerValue: integer|Long expected";
            }
            if (message.decimalValue != null && message.hasOwnProperty("decimalValue")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                if (typeof message.decimalValue !== "number")
                    return "decimalValue: number expected";
            }
            if (message.percentValue != null && message.hasOwnProperty("percentValue")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                if (typeof message.percentValue !== "number")
                    return "percentValue: number expected";
            }
            if (message.booleanValue != null && message.hasOwnProperty("booleanValue")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                if (typeof message.booleanValue !== "boolean")
                    return "booleanValue: boolean expected";
            }
            if (message.timestampMs != null && message.hasOwnProperty("timestampMs")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                if (!$util.isInteger(message.timestampMs) && !(message.timestampMs && $util.isInteger(message.timestampMs.low) && $util.isInteger(message.timestampMs.high)))
                    return "timestampMs: integer|Long expected";
            }
            if (message.dateValue != null && message.hasOwnProperty("dateValue")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                if (!$util.isInteger(message.dateValue) && !(message.dateValue && $util.isInteger(message.dateValue.low) && $util.isInteger(message.dateValue.high)))
                    return "dateValue: integer|Long expected";
            }
            if (message.dayDuration != null && message.hasOwnProperty("dayDuration")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                if (!$util.isInteger(message.dayDuration))
                    return "dayDuration: integer expected";
            }
            if (message.monetaryValue != null && message.hasOwnProperty("monetaryValue")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                if (typeof message.monetaryValue !== "number")
                    return "monetaryValue: number expected";
            }
            if (message.durationMs != null && message.hasOwnProperty("durationMs")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                if (!$util.isInteger(message.durationMs) && !(message.durationMs && $util.isInteger(message.durationMs.low) && $util.isInteger(message.durationMs.high)))
                    return "durationMs: integer|Long expected";
            }
            if (message.nullValue != null && message.hasOwnProperty("nullValue")) {
                if (properties.value === 1)
                    return "value: multiple values";
                properties.value = 1;
                switch (message.nullValue) {
                default:
                    return "nullValue: enum value expected";
                case 0:
                    break;
                }
            }
            return null;
        };

        /**
         * Creates a Scalar message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.Scalar
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.Scalar} Scalar
         */
        Scalar.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.Scalar)
                return object;
            let message = new $root.epoch_proto.Scalar();
            if (object.stringValue != null)
                message.stringValue = String(object.stringValue);
            if (object.integerValue != null)
                if ($util.Long)
                    (message.integerValue = $util.Long.fromValue(object.integerValue)).unsigned = false;
                else if (typeof object.integerValue === "string")
                    message.integerValue = parseInt(object.integerValue, 10);
                else if (typeof object.integerValue === "number")
                    message.integerValue = object.integerValue;
                else if (typeof object.integerValue === "object")
                    message.integerValue = new $util.LongBits(object.integerValue.low >>> 0, object.integerValue.high >>> 0).toNumber();
            if (object.decimalValue != null)
                message.decimalValue = Number(object.decimalValue);
            if (object.percentValue != null)
                message.percentValue = Number(object.percentValue);
            if (object.booleanValue != null)
                message.booleanValue = Boolean(object.booleanValue);
            if (object.timestampMs != null)
                if ($util.Long)
                    (message.timestampMs = $util.Long.fromValue(object.timestampMs)).unsigned = false;
                else if (typeof object.timestampMs === "string")
                    message.timestampMs = parseInt(object.timestampMs, 10);
                else if (typeof object.timestampMs === "number")
                    message.timestampMs = object.timestampMs;
                else if (typeof object.timestampMs === "object")
                    message.timestampMs = new $util.LongBits(object.timestampMs.low >>> 0, object.timestampMs.high >>> 0).toNumber();
            if (object.dateValue != null)
                if ($util.Long)
                    (message.dateValue = $util.Long.fromValue(object.dateValue)).unsigned = false;
                else if (typeof object.dateValue === "string")
                    message.dateValue = parseInt(object.dateValue, 10);
                else if (typeof object.dateValue === "number")
                    message.dateValue = object.dateValue;
                else if (typeof object.dateValue === "object")
                    message.dateValue = new $util.LongBits(object.dateValue.low >>> 0, object.dateValue.high >>> 0).toNumber();
            if (object.dayDuration != null)
                message.dayDuration = object.dayDuration | 0;
            if (object.monetaryValue != null)
                message.monetaryValue = Number(object.monetaryValue);
            if (object.durationMs != null)
                if ($util.Long)
                    (message.durationMs = $util.Long.fromValue(object.durationMs)).unsigned = false;
                else if (typeof object.durationMs === "string")
                    message.durationMs = parseInt(object.durationMs, 10);
                else if (typeof object.durationMs === "number")
                    message.durationMs = object.durationMs;
                else if (typeof object.durationMs === "object")
                    message.durationMs = new $util.LongBits(object.durationMs.low >>> 0, object.durationMs.high >>> 0).toNumber();
            switch (object.nullValue) {
            default:
                if (typeof object.nullValue === "number") {
                    message.nullValue = object.nullValue;
                    break;
                }
                break;
            case "NULL_VALUE":
            case 0:
                message.nullValue = 0;
                break;
            }
            return message;
        };

        /**
         * Creates a plain object from a Scalar message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.Scalar
         * @static
         * @param {epoch_proto.Scalar} message Scalar
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Scalar.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (message.stringValue != null && message.hasOwnProperty("stringValue")) {
                object.stringValue = message.stringValue;
                if (options.oneofs)
                    object.value = "stringValue";
            }
            if (message.integerValue != null && message.hasOwnProperty("integerValue")) {
                if (typeof message.integerValue === "number")
                    object.integerValue = options.longs === String ? String(message.integerValue) : message.integerValue;
                else
                    object.integerValue = options.longs === String ? $util.Long.prototype.toString.call(message.integerValue) : options.longs === Number ? new $util.LongBits(message.integerValue.low >>> 0, message.integerValue.high >>> 0).toNumber() : message.integerValue;
                if (options.oneofs)
                    object.value = "integerValue";
            }
            if (message.decimalValue != null && message.hasOwnProperty("decimalValue")) {
                object.decimalValue = options.json && !isFinite(message.decimalValue) ? String(message.decimalValue) : message.decimalValue;
                if (options.oneofs)
                    object.value = "decimalValue";
            }
            if (message.percentValue != null && message.hasOwnProperty("percentValue")) {
                object.percentValue = options.json && !isFinite(message.percentValue) ? String(message.percentValue) : message.percentValue;
                if (options.oneofs)
                    object.value = "percentValue";
            }
            if (message.booleanValue != null && message.hasOwnProperty("booleanValue")) {
                object.booleanValue = message.booleanValue;
                if (options.oneofs)
                    object.value = "booleanValue";
            }
            if (message.timestampMs != null && message.hasOwnProperty("timestampMs")) {
                if (typeof message.timestampMs === "number")
                    object.timestampMs = options.longs === String ? String(message.timestampMs) : message.timestampMs;
                else
                    object.timestampMs = options.longs === String ? $util.Long.prototype.toString.call(message.timestampMs) : options.longs === Number ? new $util.LongBits(message.timestampMs.low >>> 0, message.timestampMs.high >>> 0).toNumber() : message.timestampMs;
                if (options.oneofs)
                    object.value = "timestampMs";
            }
            if (message.dateValue != null && message.hasOwnProperty("dateValue")) {
                if (typeof message.dateValue === "number")
                    object.dateValue = options.longs === String ? String(message.dateValue) : message.dateValue;
                else
                    object.dateValue = options.longs === String ? $util.Long.prototype.toString.call(message.dateValue) : options.longs === Number ? new $util.LongBits(message.dateValue.low >>> 0, message.dateValue.high >>> 0).toNumber() : message.dateValue;
                if (options.oneofs)
                    object.value = "dateValue";
            }
            if (message.dayDuration != null && message.hasOwnProperty("dayDuration")) {
                object.dayDuration = message.dayDuration;
                if (options.oneofs)
                    object.value = "dayDuration";
            }
            if (message.monetaryValue != null && message.hasOwnProperty("monetaryValue")) {
                object.monetaryValue = options.json && !isFinite(message.monetaryValue) ? String(message.monetaryValue) : message.monetaryValue;
                if (options.oneofs)
                    object.value = "monetaryValue";
            }
            if (message.durationMs != null && message.hasOwnProperty("durationMs")) {
                if (typeof message.durationMs === "number")
                    object.durationMs = options.longs === String ? String(message.durationMs) : message.durationMs;
                else
                    object.durationMs = options.longs === String ? $util.Long.prototype.toString.call(message.durationMs) : options.longs === Number ? new $util.LongBits(message.durationMs.low >>> 0, message.durationMs.high >>> 0).toNumber() : message.durationMs;
                if (options.oneofs)
                    object.value = "durationMs";
            }
            if (message.nullValue != null && message.hasOwnProperty("nullValue")) {
                object.nullValue = options.enums === String ? $root.epoch_proto.NullValue[message.nullValue] === undefined ? message.nullValue : $root.epoch_proto.NullValue[message.nullValue] : message.nullValue;
                if (options.oneofs)
                    object.value = "nullValue";
            }
            return object;
        };

        /**
         * Converts this Scalar to JSON.
         * @function toJSON
         * @memberof epoch_proto.Scalar
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Scalar.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for Scalar
         * @function getTypeUrl
         * @memberof epoch_proto.Scalar
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        Scalar.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.Scalar";
        };

        return Scalar;
    })();

    epoch_proto.Array = (function() {

        /**
         * Properties of an Array.
         * @memberof epoch_proto
         * @interface IArray
         * @property {Array.<epoch_proto.IScalar>|null} [values] Array values
         */

        /**
         * Constructs a new Array.
         * @memberof epoch_proto
         * @classdesc Represents an Array.
         * @implements IArray
         * @constructor
         * @param {epoch_proto.IArray=} [properties] Properties to set
         */
        function Array(properties) {
            this.values = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Array values.
         * @member {Array.<epoch_proto.IScalar>} values
         * @memberof epoch_proto.Array
         * @instance
         */
        Array.prototype.values = $util.emptyArray;

        /**
         * Creates a new Array instance using the specified properties.
         * @function create
         * @memberof epoch_proto.Array
         * @static
         * @param {epoch_proto.IArray=} [properties] Properties to set
         * @returns {epoch_proto.Array} Array instance
         */
        Array.create = function create(properties) {
            return new Array(properties);
        };

        /**
         * Encodes the specified Array message. Does not implicitly {@link epoch_proto.Array.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.Array
         * @static
         * @param {epoch_proto.IArray} message Array message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Array.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.values != null && message.values.length)
                for (let i = 0; i < message.values.length; ++i)
                    $root.epoch_proto.Scalar.encode(message.values[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified Array message, length delimited. Does not implicitly {@link epoch_proto.Array.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.Array
         * @static
         * @param {epoch_proto.IArray} message Array message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Array.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an Array message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.Array
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.Array} Array
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Array.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.Array();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.values && message.values.length))
                            message.values = [];
                        message.values.push($root.epoch_proto.Scalar.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an Array message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.Array
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.Array} Array
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Array.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an Array message.
         * @function verify
         * @memberof epoch_proto.Array
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Array.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.values != null && message.hasOwnProperty("values")) {
                if (!Array.isArray(message.values))
                    return "values: array expected";
                for (let i = 0; i < message.values.length; ++i) {
                    let error = $root.epoch_proto.Scalar.verify(message.values[i]);
                    if (error)
                        return "values." + error;
                }
            }
            return null;
        };

        /**
         * Creates an Array message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.Array
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.Array} Array
         */
        Array.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.Array)
                return object;
            let message = new $root.epoch_proto.Array();
            if (object.values) {
                if (!Array.isArray(object.values))
                    throw TypeError(".epoch_proto.Array.values: array expected");
                message.values = [];
                for (let i = 0; i < object.values.length; ++i) {
                    if (typeof object.values[i] !== "object")
                        throw TypeError(".epoch_proto.Array.values: object expected");
                    message.values[i] = $root.epoch_proto.Scalar.fromObject(object.values[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from an Array message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.Array
         * @static
         * @param {epoch_proto.Array} message Array
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Array.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.values = [];
            if (message.values && message.values.length) {
                object.values = [];
                for (let j = 0; j < message.values.length; ++j)
                    object.values[j] = $root.epoch_proto.Scalar.toObject(message.values[j], options);
            }
            return object;
        };

        /**
         * Converts this Array to JSON.
         * @function toJSON
         * @memberof epoch_proto.Array
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Array.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for Array
         * @function getTypeUrl
         * @memberof epoch_proto.Array
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        Array.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.Array";
        };

        return Array;
    })();

    /**
     * AxisType enum.
     * @name epoch_proto.AxisType
     * @enum {number}
     * @property {number} AxisUnspecified=0 AxisUnspecified value
     * @property {number} AxisLinear=1 AxisLinear value
     * @property {number} AxisLogarithmic=2 AxisLogarithmic value
     * @property {number} AxisDateTime=3 AxisDateTime value
     * @property {number} AxisCategory=4 AxisCategory value
     */
    epoch_proto.AxisType = (function() {
        const valuesById = {}, values = Object.create(valuesById);
        values[valuesById[0] = "AxisUnspecified"] = 0;
        values[valuesById[1] = "AxisLinear"] = 1;
        values[valuesById[2] = "AxisLogarithmic"] = 2;
        values[valuesById[3] = "AxisDateTime"] = 3;
        values[valuesById[4] = "AxisCategory"] = 4;
        return values;
    })();

    /**
     * DashStyle enum.
     * @name epoch_proto.DashStyle
     * @enum {number}
     * @property {number} DashStyleUnspecified=0 DashStyleUnspecified value
     * @property {number} Solid=1 Solid value
     * @property {number} ShortDash=2 ShortDash value
     * @property {number} ShortDot=3 ShortDot value
     * @property {number} ShortDashDot=4 ShortDashDot value
     * @property {number} ShortDashDotDot=5 ShortDashDotDot value
     * @property {number} Dot=6 Dot value
     * @property {number} Dash=7 Dash value
     * @property {number} LongDash=8 LongDash value
     * @property {number} DashDot=9 DashDot value
     * @property {number} LongDashDot=10 LongDashDot value
     * @property {number} LongDashDotDot=11 LongDashDotDot value
     */
    epoch_proto.DashStyle = (function() {
        const valuesById = {}, values = Object.create(valuesById);
        values[valuesById[0] = "DashStyleUnspecified"] = 0;
        values[valuesById[1] = "Solid"] = 1;
        values[valuesById[2] = "ShortDash"] = 2;
        values[valuesById[3] = "ShortDot"] = 3;
        values[valuesById[4] = "ShortDashDot"] = 4;
        values[valuesById[5] = "ShortDashDotDot"] = 5;
        values[valuesById[6] = "Dot"] = 6;
        values[valuesById[7] = "Dash"] = 7;
        values[valuesById[8] = "LongDash"] = 8;
        values[valuesById[9] = "DashDot"] = 9;
        values[valuesById[10] = "LongDashDot"] = 10;
        values[valuesById[11] = "LongDashDotDot"] = 11;
        return values;
    })();

    epoch_proto.AxisDef = (function() {

        /**
         * Properties of an AxisDef.
         * @memberof epoch_proto
         * @interface IAxisDef
         * @property {epoch_proto.AxisType|null} [type] AxisDef type
         * @property {string|null} [label] AxisDef label
         * @property {Array.<string>|null} [categories] AxisDef categories
         */

        /**
         * Constructs a new AxisDef.
         * @memberof epoch_proto
         * @classdesc Represents an AxisDef.
         * @implements IAxisDef
         * @constructor
         * @param {epoch_proto.IAxisDef=} [properties] Properties to set
         */
        function AxisDef(properties) {
            this.categories = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * AxisDef type.
         * @member {epoch_proto.AxisType|null|undefined} type
         * @memberof epoch_proto.AxisDef
         * @instance
         */
        AxisDef.prototype.type = null;

        /**
         * AxisDef label.
         * @member {string|null|undefined} label
         * @memberof epoch_proto.AxisDef
         * @instance
         */
        AxisDef.prototype.label = null;

        /**
         * AxisDef categories.
         * @member {Array.<string>} categories
         * @memberof epoch_proto.AxisDef
         * @instance
         */
        AxisDef.prototype.categories = $util.emptyArray;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(AxisDef.prototype, "_type", {
            get: $util.oneOfGetter($oneOfFields = ["type"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(AxisDef.prototype, "_label", {
            get: $util.oneOfGetter($oneOfFields = ["label"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new AxisDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.AxisDef
         * @static
         * @param {epoch_proto.IAxisDef=} [properties] Properties to set
         * @returns {epoch_proto.AxisDef} AxisDef instance
         */
        AxisDef.create = function create(properties) {
            return new AxisDef(properties);
        };

        /**
         * Encodes the specified AxisDef message. Does not implicitly {@link epoch_proto.AxisDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.AxisDef
         * @static
         * @param {epoch_proto.IAxisDef} message AxisDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AxisDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.type != null && Object.hasOwnProperty.call(message, "type"))
                writer.uint32(/* id 1, wireType 0 =*/8).int32(message.type);
            if (message.label != null && Object.hasOwnProperty.call(message, "label"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.label);
            if (message.categories != null && message.categories.length)
                for (let i = 0; i < message.categories.length; ++i)
                    writer.uint32(/* id 3, wireType 2 =*/26).string(message.categories[i]);
            return writer;
        };

        /**
         * Encodes the specified AxisDef message, length delimited. Does not implicitly {@link epoch_proto.AxisDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.AxisDef
         * @static
         * @param {epoch_proto.IAxisDef} message AxisDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AxisDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an AxisDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.AxisDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.AxisDef} AxisDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AxisDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.AxisDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.type = reader.int32();
                        break;
                    }
                case 2: {
                        message.label = reader.string();
                        break;
                    }
                case 3: {
                        if (!(message.categories && message.categories.length))
                            message.categories = [];
                        message.categories.push(reader.string());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an AxisDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.AxisDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.AxisDef} AxisDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AxisDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an AxisDef message.
         * @function verify
         * @memberof epoch_proto.AxisDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        AxisDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.type != null && message.hasOwnProperty("type")) {
                properties._type = 1;
                switch (message.type) {
                default:
                    return "type: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                    break;
                }
            }
            if (message.label != null && message.hasOwnProperty("label")) {
                properties._label = 1;
                if (!$util.isString(message.label))
                    return "label: string expected";
            }
            if (message.categories != null && message.hasOwnProperty("categories")) {
                if (!Array.isArray(message.categories))
                    return "categories: array expected";
                for (let i = 0; i < message.categories.length; ++i)
                    if (!$util.isString(message.categories[i]))
                        return "categories: string[] expected";
            }
            return null;
        };

        /**
         * Creates an AxisDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.AxisDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.AxisDef} AxisDef
         */
        AxisDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.AxisDef)
                return object;
            let message = new $root.epoch_proto.AxisDef();
            switch (object.type) {
            default:
                if (typeof object.type === "number") {
                    message.type = object.type;
                    break;
                }
                break;
            case "AxisUnspecified":
            case 0:
                message.type = 0;
                break;
            case "AxisLinear":
            case 1:
                message.type = 1;
                break;
            case "AxisLogarithmic":
            case 2:
                message.type = 2;
                break;
            case "AxisDateTime":
            case 3:
                message.type = 3;
                break;
            case "AxisCategory":
            case 4:
                message.type = 4;
                break;
            }
            if (object.label != null)
                message.label = String(object.label);
            if (object.categories) {
                if (!Array.isArray(object.categories))
                    throw TypeError(".epoch_proto.AxisDef.categories: array expected");
                message.categories = [];
                for (let i = 0; i < object.categories.length; ++i)
                    message.categories[i] = String(object.categories[i]);
            }
            return message;
        };

        /**
         * Creates a plain object from an AxisDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.AxisDef
         * @static
         * @param {epoch_proto.AxisDef} message AxisDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        AxisDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.categories = [];
            if (message.type != null && message.hasOwnProperty("type")) {
                object.type = options.enums === String ? $root.epoch_proto.AxisType[message.type] === undefined ? message.type : $root.epoch_proto.AxisType[message.type] : message.type;
                if (options.oneofs)
                    object._type = "type";
            }
            if (message.label != null && message.hasOwnProperty("label")) {
                object.label = message.label;
                if (options.oneofs)
                    object._label = "label";
            }
            if (message.categories && message.categories.length) {
                object.categories = [];
                for (let j = 0; j < message.categories.length; ++j)
                    object.categories[j] = message.categories[j];
            }
            return object;
        };

        /**
         * Converts this AxisDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.AxisDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        AxisDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for AxisDef
         * @function getTypeUrl
         * @memberof epoch_proto.AxisDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        AxisDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.AxisDef";
        };

        return AxisDef;
    })();

    epoch_proto.ChartDef = (function() {

        /**
         * Properties of a ChartDef.
         * @memberof epoch_proto
         * @interface IChartDef
         * @property {string|null} [id] ChartDef id
         * @property {string|null} [title] ChartDef title
         * @property {epoch_proto.EpochFolioDashboardWidget|null} [type] ChartDef type
         * @property {string|null} [category] ChartDef category
         * @property {epoch_proto.IAxisDef|null} [yAxis] ChartDef yAxis
         * @property {epoch_proto.IAxisDef|null} [xAxis] ChartDef xAxis
         */

        /**
         * Constructs a new ChartDef.
         * @memberof epoch_proto
         * @classdesc Represents a ChartDef.
         * @implements IChartDef
         * @constructor
         * @param {epoch_proto.IChartDef=} [properties] Properties to set
         */
        function ChartDef(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ChartDef id.
         * @member {string} id
         * @memberof epoch_proto.ChartDef
         * @instance
         */
        ChartDef.prototype.id = "";

        /**
         * ChartDef title.
         * @member {string} title
         * @memberof epoch_proto.ChartDef
         * @instance
         */
        ChartDef.prototype.title = "";

        /**
         * ChartDef type.
         * @member {epoch_proto.EpochFolioDashboardWidget} type
         * @memberof epoch_proto.ChartDef
         * @instance
         */
        ChartDef.prototype.type = 0;

        /**
         * ChartDef category.
         * @member {string} category
         * @memberof epoch_proto.ChartDef
         * @instance
         */
        ChartDef.prototype.category = "";

        /**
         * ChartDef yAxis.
         * @member {epoch_proto.IAxisDef|null|undefined} yAxis
         * @memberof epoch_proto.ChartDef
         * @instance
         */
        ChartDef.prototype.yAxis = null;

        /**
         * ChartDef xAxis.
         * @member {epoch_proto.IAxisDef|null|undefined} xAxis
         * @memberof epoch_proto.ChartDef
         * @instance
         */
        ChartDef.prototype.xAxis = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(ChartDef.prototype, "_yAxis", {
            get: $util.oneOfGetter($oneOfFields = ["yAxis"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(ChartDef.prototype, "_xAxis", {
            get: $util.oneOfGetter($oneOfFields = ["xAxis"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new ChartDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.ChartDef
         * @static
         * @param {epoch_proto.IChartDef=} [properties] Properties to set
         * @returns {epoch_proto.ChartDef} ChartDef instance
         */
        ChartDef.create = function create(properties) {
            return new ChartDef(properties);
        };

        /**
         * Encodes the specified ChartDef message. Does not implicitly {@link epoch_proto.ChartDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.ChartDef
         * @static
         * @param {epoch_proto.IChartDef} message ChartDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ChartDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.title != null && Object.hasOwnProperty.call(message, "title"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.title);
            if (message.type != null && Object.hasOwnProperty.call(message, "type"))
                writer.uint32(/* id 3, wireType 0 =*/24).int32(message.type);
            if (message.category != null && Object.hasOwnProperty.call(message, "category"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.category);
            if (message.yAxis != null && Object.hasOwnProperty.call(message, "yAxis"))
                $root.epoch_proto.AxisDef.encode(message.yAxis, writer.uint32(/* id 5, wireType 2 =*/42).fork()).ldelim();
            if (message.xAxis != null && Object.hasOwnProperty.call(message, "xAxis"))
                $root.epoch_proto.AxisDef.encode(message.xAxis, writer.uint32(/* id 6, wireType 2 =*/50).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ChartDef message, length delimited. Does not implicitly {@link epoch_proto.ChartDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.ChartDef
         * @static
         * @param {epoch_proto.IChartDef} message ChartDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ChartDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ChartDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.ChartDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.ChartDef} ChartDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ChartDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.ChartDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.title = reader.string();
                        break;
                    }
                case 3: {
                        message.type = reader.int32();
                        break;
                    }
                case 4: {
                        message.category = reader.string();
                        break;
                    }
                case 5: {
                        message.yAxis = $root.epoch_proto.AxisDef.decode(reader, reader.uint32());
                        break;
                    }
                case 6: {
                        message.xAxis = $root.epoch_proto.AxisDef.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ChartDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.ChartDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.ChartDef} ChartDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ChartDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ChartDef message.
         * @function verify
         * @memberof epoch_proto.ChartDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ChartDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.title != null && message.hasOwnProperty("title"))
                if (!$util.isString(message.title))
                    return "title: string expected";
            if (message.type != null && message.hasOwnProperty("type"))
                switch (message.type) {
                default:
                    return "type: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                case 6:
                case 7:
                case 8:
                case 9:
                case 10:
                case 11:
                case 12:
                case 13:
                case 14:
                case 15:
                case 16:
                case 17:
                case 18:
                case 19:
                case 20:
                case 21:
                case 22:
                case 23:
                case 24:
                    break;
                }
            if (message.category != null && message.hasOwnProperty("category"))
                if (!$util.isString(message.category))
                    return "category: string expected";
            if (message.yAxis != null && message.hasOwnProperty("yAxis")) {
                properties._yAxis = 1;
                {
                    let error = $root.epoch_proto.AxisDef.verify(message.yAxis);
                    if (error)
                        return "yAxis." + error;
                }
            }
            if (message.xAxis != null && message.hasOwnProperty("xAxis")) {
                properties._xAxis = 1;
                {
                    let error = $root.epoch_proto.AxisDef.verify(message.xAxis);
                    if (error)
                        return "xAxis." + error;
                }
            }
            return null;
        };

        /**
         * Creates a ChartDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.ChartDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.ChartDef} ChartDef
         */
        ChartDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.ChartDef)
                return object;
            let message = new $root.epoch_proto.ChartDef();
            if (object.id != null)
                message.id = String(object.id);
            if (object.title != null)
                message.title = String(object.title);
            switch (object.type) {
            default:
                if (typeof object.type === "number") {
                    message.type = object.type;
                    break;
                }
                break;
            case "WidgetUnspecified":
            case 0:
                message.type = 0;
                break;
            case "WidgetCard":
            case 1:
                message.type = 1;
                break;
            case "WidgetLines":
            case 2:
                message.type = 2;
                break;
            case "WidgetBar":
            case 3:
                message.type = 3;
                break;
            case "WidgetDataTable":
            case 4:
                message.type = 4;
                break;
            case "WidgetXRange":
            case 5:
                message.type = 5;
                break;
            case "WidgetHistogram":
            case 6:
                message.type = 6;
                break;
            case "WidgetPie":
            case 7:
                message.type = 7;
                break;
            case "WidgetHeatMap":
            case 8:
                message.type = 8;
                break;
            case "WidgetBoxPlot":
            case 9:
                message.type = 9;
                break;
            case "WidgetArea":
            case 10:
                message.type = 10;
                break;
            case "WidgetColumn":
            case 11:
                message.type = 11;
                break;
            case "WidgetScatter":
            case 12:
                message.type = 12;
                break;
            case "WidgetWaterfall":
            case 13:
                message.type = 13;
                break;
            case "WidgetSpline":
            case 14:
                message.type = 14;
                break;
            case "WidgetBubble":
            case 15:
                message.type = 15;
                break;
            case "WidgetTreemap":
            case 16:
                message.type = 16;
                break;
            case "WidgetSankey":
            case 17:
                message.type = 17;
                break;
            case "WidgetAreaRange":
            case 18:
                message.type = 18;
                break;
            case "WidgetGauge":
            case 19:
                message.type = 19;
                break;
            case "WidgetBullet":
            case 20:
                message.type = 20;
                break;
            case "WidgetTimeline":
            case 21:
                message.type = 21;
                break;
            case "WidgetErrorBar":
            case 22:
                message.type = 22;
                break;
            case "WidgetBellCurve":
            case 23:
                message.type = 23;
                break;
            case "WidgetNumericErrorBar":
            case 24:
                message.type = 24;
                break;
            }
            if (object.category != null)
                message.category = String(object.category);
            if (object.yAxis != null) {
                if (typeof object.yAxis !== "object")
                    throw TypeError(".epoch_proto.ChartDef.yAxis: object expected");
                message.yAxis = $root.epoch_proto.AxisDef.fromObject(object.yAxis);
            }
            if (object.xAxis != null) {
                if (typeof object.xAxis !== "object")
                    throw TypeError(".epoch_proto.ChartDef.xAxis: object expected");
                message.xAxis = $root.epoch_proto.AxisDef.fromObject(object.xAxis);
            }
            return message;
        };

        /**
         * Creates a plain object from a ChartDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.ChartDef
         * @static
         * @param {epoch_proto.ChartDef} message ChartDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ChartDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.id = "";
                object.title = "";
                object.type = options.enums === String ? "WidgetUnspecified" : 0;
                object.category = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.title != null && message.hasOwnProperty("title"))
                object.title = message.title;
            if (message.type != null && message.hasOwnProperty("type"))
                object.type = options.enums === String ? $root.epoch_proto.EpochFolioDashboardWidget[message.type] === undefined ? message.type : $root.epoch_proto.EpochFolioDashboardWidget[message.type] : message.type;
            if (message.category != null && message.hasOwnProperty("category"))
                object.category = message.category;
            if (message.yAxis != null && message.hasOwnProperty("yAxis")) {
                object.yAxis = $root.epoch_proto.AxisDef.toObject(message.yAxis, options);
                if (options.oneofs)
                    object._yAxis = "yAxis";
            }
            if (message.xAxis != null && message.hasOwnProperty("xAxis")) {
                object.xAxis = $root.epoch_proto.AxisDef.toObject(message.xAxis, options);
                if (options.oneofs)
                    object._xAxis = "xAxis";
            }
            return object;
        };

        /**
         * Converts this ChartDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.ChartDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ChartDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ChartDef
         * @function getTypeUrl
         * @memberof epoch_proto.ChartDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ChartDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.ChartDef";
        };

        return ChartDef;
    })();

    epoch_proto.StraightLineDef = (function() {

        /**
         * Properties of a StraightLineDef.
         * @memberof epoch_proto
         * @interface IStraightLineDef
         * @property {string|null} [title] StraightLineDef title
         * @property {number|null} [value] StraightLineDef value
         * @property {boolean|null} [vertical] StraightLineDef vertical
         */

        /**
         * Constructs a new StraightLineDef.
         * @memberof epoch_proto
         * @classdesc Represents a StraightLineDef.
         * @implements IStraightLineDef
         * @constructor
         * @param {epoch_proto.IStraightLineDef=} [properties] Properties to set
         */
        function StraightLineDef(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * StraightLineDef title.
         * @member {string} title
         * @memberof epoch_proto.StraightLineDef
         * @instance
         */
        StraightLineDef.prototype.title = "";

        /**
         * StraightLineDef value.
         * @member {number} value
         * @memberof epoch_proto.StraightLineDef
         * @instance
         */
        StraightLineDef.prototype.value = 0;

        /**
         * StraightLineDef vertical.
         * @member {boolean} vertical
         * @memberof epoch_proto.StraightLineDef
         * @instance
         */
        StraightLineDef.prototype.vertical = false;

        /**
         * Creates a new StraightLineDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.StraightLineDef
         * @static
         * @param {epoch_proto.IStraightLineDef=} [properties] Properties to set
         * @returns {epoch_proto.StraightLineDef} StraightLineDef instance
         */
        StraightLineDef.create = function create(properties) {
            return new StraightLineDef(properties);
        };

        /**
         * Encodes the specified StraightLineDef message. Does not implicitly {@link epoch_proto.StraightLineDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.StraightLineDef
         * @static
         * @param {epoch_proto.IStraightLineDef} message StraightLineDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        StraightLineDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.title != null && Object.hasOwnProperty.call(message, "title"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.title);
            if (message.value != null && Object.hasOwnProperty.call(message, "value"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.value);
            if (message.vertical != null && Object.hasOwnProperty.call(message, "vertical"))
                writer.uint32(/* id 3, wireType 0 =*/24).bool(message.vertical);
            return writer;
        };

        /**
         * Encodes the specified StraightLineDef message, length delimited. Does not implicitly {@link epoch_proto.StraightLineDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.StraightLineDef
         * @static
         * @param {epoch_proto.IStraightLineDef} message StraightLineDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        StraightLineDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a StraightLineDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.StraightLineDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.StraightLineDef} StraightLineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        StraightLineDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.StraightLineDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.title = reader.string();
                        break;
                    }
                case 2: {
                        message.value = reader.double();
                        break;
                    }
                case 3: {
                        message.vertical = reader.bool();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a StraightLineDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.StraightLineDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.StraightLineDef} StraightLineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        StraightLineDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a StraightLineDef message.
         * @function verify
         * @memberof epoch_proto.StraightLineDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        StraightLineDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.title != null && message.hasOwnProperty("title"))
                if (!$util.isString(message.title))
                    return "title: string expected";
            if (message.value != null && message.hasOwnProperty("value"))
                if (typeof message.value !== "number")
                    return "value: number expected";
            if (message.vertical != null && message.hasOwnProperty("vertical"))
                if (typeof message.vertical !== "boolean")
                    return "vertical: boolean expected";
            return null;
        };

        /**
         * Creates a StraightLineDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.StraightLineDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.StraightLineDef} StraightLineDef
         */
        StraightLineDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.StraightLineDef)
                return object;
            let message = new $root.epoch_proto.StraightLineDef();
            if (object.title != null)
                message.title = String(object.title);
            if (object.value != null)
                message.value = Number(object.value);
            if (object.vertical != null)
                message.vertical = Boolean(object.vertical);
            return message;
        };

        /**
         * Creates a plain object from a StraightLineDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.StraightLineDef
         * @static
         * @param {epoch_proto.StraightLineDef} message StraightLineDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        StraightLineDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.title = "";
                object.value = 0;
                object.vertical = false;
            }
            if (message.title != null && message.hasOwnProperty("title"))
                object.title = message.title;
            if (message.value != null && message.hasOwnProperty("value"))
                object.value = options.json && !isFinite(message.value) ? String(message.value) : message.value;
            if (message.vertical != null && message.hasOwnProperty("vertical"))
                object.vertical = message.vertical;
            return object;
        };

        /**
         * Converts this StraightLineDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.StraightLineDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        StraightLineDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for StraightLineDef
         * @function getTypeUrl
         * @memberof epoch_proto.StraightLineDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        StraightLineDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.StraightLineDef";
        };

        return StraightLineDef;
    })();

    epoch_proto.Band = (function() {

        /**
         * Properties of a Band.
         * @memberof epoch_proto
         * @interface IBand
         * @property {epoch_proto.IScalar|null} [from] Band from
         * @property {epoch_proto.IScalar|null} [to] Band to
         */

        /**
         * Constructs a new Band.
         * @memberof epoch_proto
         * @classdesc Represents a Band.
         * @implements IBand
         * @constructor
         * @param {epoch_proto.IBand=} [properties] Properties to set
         */
        function Band(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Band from.
         * @member {epoch_proto.IScalar|null|undefined} from
         * @memberof epoch_proto.Band
         * @instance
         */
        Band.prototype.from = null;

        /**
         * Band to.
         * @member {epoch_proto.IScalar|null|undefined} to
         * @memberof epoch_proto.Band
         * @instance
         */
        Band.prototype.to = null;

        /**
         * Creates a new Band instance using the specified properties.
         * @function create
         * @memberof epoch_proto.Band
         * @static
         * @param {epoch_proto.IBand=} [properties] Properties to set
         * @returns {epoch_proto.Band} Band instance
         */
        Band.create = function create(properties) {
            return new Band(properties);
        };

        /**
         * Encodes the specified Band message. Does not implicitly {@link epoch_proto.Band.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.Band
         * @static
         * @param {epoch_proto.IBand} message Band message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Band.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.from != null && Object.hasOwnProperty.call(message, "from"))
                $root.epoch_proto.Scalar.encode(message.from, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.to != null && Object.hasOwnProperty.call(message, "to"))
                $root.epoch_proto.Scalar.encode(message.to, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified Band message, length delimited. Does not implicitly {@link epoch_proto.Band.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.Band
         * @static
         * @param {epoch_proto.IBand} message Band message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Band.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a Band message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.Band
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.Band} Band
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Band.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.Band();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.from = $root.epoch_proto.Scalar.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        message.to = $root.epoch_proto.Scalar.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a Band message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.Band
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.Band} Band
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Band.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a Band message.
         * @function verify
         * @memberof epoch_proto.Band
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Band.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.from != null && message.hasOwnProperty("from")) {
                let error = $root.epoch_proto.Scalar.verify(message.from);
                if (error)
                    return "from." + error;
            }
            if (message.to != null && message.hasOwnProperty("to")) {
                let error = $root.epoch_proto.Scalar.verify(message.to);
                if (error)
                    return "to." + error;
            }
            return null;
        };

        /**
         * Creates a Band message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.Band
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.Band} Band
         */
        Band.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.Band)
                return object;
            let message = new $root.epoch_proto.Band();
            if (object.from != null) {
                if (typeof object.from !== "object")
                    throw TypeError(".epoch_proto.Band.from: object expected");
                message.from = $root.epoch_proto.Scalar.fromObject(object.from);
            }
            if (object.to != null) {
                if (typeof object.to !== "object")
                    throw TypeError(".epoch_proto.Band.to: object expected");
                message.to = $root.epoch_proto.Scalar.fromObject(object.to);
            }
            return message;
        };

        /**
         * Creates a plain object from a Band message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.Band
         * @static
         * @param {epoch_proto.Band} message Band
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Band.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.from = null;
                object.to = null;
            }
            if (message.from != null && message.hasOwnProperty("from"))
                object.from = $root.epoch_proto.Scalar.toObject(message.from, options);
            if (message.to != null && message.hasOwnProperty("to"))
                object.to = $root.epoch_proto.Scalar.toObject(message.to, options);
            return object;
        };

        /**
         * Converts this Band to JSON.
         * @function toJSON
         * @memberof epoch_proto.Band
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Band.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for Band
         * @function getTypeUrl
         * @memberof epoch_proto.Band
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        Band.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.Band";
        };

        return Band;
    })();

    epoch_proto.Point = (function() {

        /**
         * Properties of a Point.
         * @memberof epoch_proto
         * @interface IPoint
         * @property {number|Long|null} [x] Point x
         * @property {number|null} [y] Point y
         */

        /**
         * Constructs a new Point.
         * @memberof epoch_proto
         * @classdesc Represents a Point.
         * @implements IPoint
         * @constructor
         * @param {epoch_proto.IPoint=} [properties] Properties to set
         */
        function Point(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Point x.
         * @member {number|Long} x
         * @memberof epoch_proto.Point
         * @instance
         */
        Point.prototype.x = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * Point y.
         * @member {number} y
         * @memberof epoch_proto.Point
         * @instance
         */
        Point.prototype.y = 0;

        /**
         * Creates a new Point instance using the specified properties.
         * @function create
         * @memberof epoch_proto.Point
         * @static
         * @param {epoch_proto.IPoint=} [properties] Properties to set
         * @returns {epoch_proto.Point} Point instance
         */
        Point.create = function create(properties) {
            return new Point(properties);
        };

        /**
         * Encodes the specified Point message. Does not implicitly {@link epoch_proto.Point.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.Point
         * @static
         * @param {epoch_proto.IPoint} message Point message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Point.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 0 =*/8).int64(message.x);
            if (message.y != null && Object.hasOwnProperty.call(message, "y"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.y);
            return writer;
        };

        /**
         * Encodes the specified Point message, length delimited. Does not implicitly {@link epoch_proto.Point.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.Point
         * @static
         * @param {epoch_proto.IPoint} message Point message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Point.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a Point message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.Point
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.Point} Point
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Point.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.Point();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.int64();
                        break;
                    }
                case 2: {
                        message.y = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a Point message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.Point
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.Point} Point
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Point.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a Point message.
         * @function verify
         * @memberof epoch_proto.Point
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Point.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.x != null && message.hasOwnProperty("x"))
                if (!$util.isInteger(message.x) && !(message.x && $util.isInteger(message.x.low) && $util.isInteger(message.x.high)))
                    return "x: integer|Long expected";
            if (message.y != null && message.hasOwnProperty("y"))
                if (typeof message.y !== "number")
                    return "y: number expected";
            return null;
        };

        /**
         * Creates a Point message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.Point
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.Point} Point
         */
        Point.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.Point)
                return object;
            let message = new $root.epoch_proto.Point();
            if (object.x != null)
                if ($util.Long)
                    (message.x = $util.Long.fromValue(object.x)).unsigned = false;
                else if (typeof object.x === "string")
                    message.x = parseInt(object.x, 10);
                else if (typeof object.x === "number")
                    message.x = object.x;
                else if (typeof object.x === "object")
                    message.x = new $util.LongBits(object.x.low >>> 0, object.x.high >>> 0).toNumber();
            if (object.y != null)
                message.y = Number(object.y);
            return message;
        };

        /**
         * Creates a plain object from a Point message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.Point
         * @static
         * @param {epoch_proto.Point} message Point
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Point.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                if ($util.Long) {
                    let long = new $util.Long(0, 0, false);
                    object.x = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.x = options.longs === String ? "0" : 0;
                object.y = 0;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x === "number")
                    object.x = options.longs === String ? String(message.x) : message.x;
                else
                    object.x = options.longs === String ? $util.Long.prototype.toString.call(message.x) : options.longs === Number ? new $util.LongBits(message.x.low >>> 0, message.x.high >>> 0).toNumber() : message.x;
            if (message.y != null && message.hasOwnProperty("y"))
                object.y = options.json && !isFinite(message.y) ? String(message.y) : message.y;
            return object;
        };

        /**
         * Converts this Point to JSON.
         * @function toJSON
         * @memberof epoch_proto.Point
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Point.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for Point
         * @function getTypeUrl
         * @memberof epoch_proto.Point
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        Point.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.Point";
        };

        return Point;
    })();

    epoch_proto.NumericPoint = (function() {

        /**
         * Properties of a NumericPoint.
         * @memberof epoch_proto
         * @interface INumericPoint
         * @property {number|null} [x] NumericPoint x
         * @property {number|null} [y] NumericPoint y
         */

        /**
         * Constructs a new NumericPoint.
         * @memberof epoch_proto
         * @classdesc Represents a NumericPoint.
         * @implements INumericPoint
         * @constructor
         * @param {epoch_proto.INumericPoint=} [properties] Properties to set
         */
        function NumericPoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NumericPoint x.
         * @member {number} x
         * @memberof epoch_proto.NumericPoint
         * @instance
         */
        NumericPoint.prototype.x = 0;

        /**
         * NumericPoint y.
         * @member {number} y
         * @memberof epoch_proto.NumericPoint
         * @instance
         */
        NumericPoint.prototype.y = 0;

        /**
         * Creates a new NumericPoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.NumericPoint
         * @static
         * @param {epoch_proto.INumericPoint=} [properties] Properties to set
         * @returns {epoch_proto.NumericPoint} NumericPoint instance
         */
        NumericPoint.create = function create(properties) {
            return new NumericPoint(properties);
        };

        /**
         * Encodes the specified NumericPoint message. Does not implicitly {@link epoch_proto.NumericPoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.NumericPoint
         * @static
         * @param {epoch_proto.INumericPoint} message NumericPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericPoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 1 =*/9).double(message.x);
            if (message.y != null && Object.hasOwnProperty.call(message, "y"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.y);
            return writer;
        };

        /**
         * Encodes the specified NumericPoint message, length delimited. Does not implicitly {@link epoch_proto.NumericPoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.NumericPoint
         * @static
         * @param {epoch_proto.INumericPoint} message NumericPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericPoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NumericPoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.NumericPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.NumericPoint} NumericPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericPoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.NumericPoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.double();
                        break;
                    }
                case 2: {
                        message.y = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NumericPoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.NumericPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.NumericPoint} NumericPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericPoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NumericPoint message.
         * @function verify
         * @memberof epoch_proto.NumericPoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NumericPoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x !== "number")
                    return "x: number expected";
            if (message.y != null && message.hasOwnProperty("y"))
                if (typeof message.y !== "number")
                    return "y: number expected";
            return null;
        };

        /**
         * Creates a NumericPoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.NumericPoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.NumericPoint} NumericPoint
         */
        NumericPoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.NumericPoint)
                return object;
            let message = new $root.epoch_proto.NumericPoint();
            if (object.x != null)
                message.x = Number(object.x);
            if (object.y != null)
                message.y = Number(object.y);
            return message;
        };

        /**
         * Creates a plain object from a NumericPoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.NumericPoint
         * @static
         * @param {epoch_proto.NumericPoint} message NumericPoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NumericPoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.x = 0;
                object.y = 0;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                object.x = options.json && !isFinite(message.x) ? String(message.x) : message.x;
            if (message.y != null && message.hasOwnProperty("y"))
                object.y = options.json && !isFinite(message.y) ? String(message.y) : message.y;
            return object;
        };

        /**
         * Converts this NumericPoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.NumericPoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NumericPoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NumericPoint
         * @function getTypeUrl
         * @memberof epoch_proto.NumericPoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NumericPoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.NumericPoint";
        };

        return NumericPoint;
    })();

    epoch_proto.Line = (function() {

        /**
         * Properties of a Line.
         * @memberof epoch_proto
         * @interface ILine
         * @property {Array.<epoch_proto.IPoint>|null} [data] Line data
         * @property {string|null} [name] Line name
         * @property {epoch_proto.DashStyle|null} [dashStyle] Line dashStyle
         * @property {number|null} [lineWidth] Line lineWidth
         */

        /**
         * Constructs a new Line.
         * @memberof epoch_proto
         * @classdesc Represents a Line.
         * @implements ILine
         * @constructor
         * @param {epoch_proto.ILine=} [properties] Properties to set
         */
        function Line(properties) {
            this.data = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Line data.
         * @member {Array.<epoch_proto.IPoint>} data
         * @memberof epoch_proto.Line
         * @instance
         */
        Line.prototype.data = $util.emptyArray;

        /**
         * Line name.
         * @member {string} name
         * @memberof epoch_proto.Line
         * @instance
         */
        Line.prototype.name = "";

        /**
         * Line dashStyle.
         * @member {epoch_proto.DashStyle|null|undefined} dashStyle
         * @memberof epoch_proto.Line
         * @instance
         */
        Line.prototype.dashStyle = null;

        /**
         * Line lineWidth.
         * @member {number|null|undefined} lineWidth
         * @memberof epoch_proto.Line
         * @instance
         */
        Line.prototype.lineWidth = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(Line.prototype, "_dashStyle", {
            get: $util.oneOfGetter($oneOfFields = ["dashStyle"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(Line.prototype, "_lineWidth", {
            get: $util.oneOfGetter($oneOfFields = ["lineWidth"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new Line instance using the specified properties.
         * @function create
         * @memberof epoch_proto.Line
         * @static
         * @param {epoch_proto.ILine=} [properties] Properties to set
         * @returns {epoch_proto.Line} Line instance
         */
        Line.create = function create(properties) {
            return new Line(properties);
        };

        /**
         * Encodes the specified Line message. Does not implicitly {@link epoch_proto.Line.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.Line
         * @static
         * @param {epoch_proto.ILine} message Line message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Line.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.Point.encode(message.data[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.name);
            if (message.dashStyle != null && Object.hasOwnProperty.call(message, "dashStyle"))
                writer.uint32(/* id 3, wireType 0 =*/24).int32(message.dashStyle);
            if (message.lineWidth != null && Object.hasOwnProperty.call(message, "lineWidth"))
                writer.uint32(/* id 4, wireType 0 =*/32).uint32(message.lineWidth);
            return writer;
        };

        /**
         * Encodes the specified Line message, length delimited. Does not implicitly {@link epoch_proto.Line.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.Line
         * @static
         * @param {epoch_proto.ILine} message Line message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Line.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a Line message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.Line
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.Line} Line
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Line.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.Line();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.Point.decode(reader, reader.uint32()));
                        break;
                    }
                case 2: {
                        message.name = reader.string();
                        break;
                    }
                case 3: {
                        message.dashStyle = reader.int32();
                        break;
                    }
                case 4: {
                        message.lineWidth = reader.uint32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a Line message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.Line
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.Line} Line
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Line.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a Line message.
         * @function verify
         * @memberof epoch_proto.Line
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Line.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.Point.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.dashStyle != null && message.hasOwnProperty("dashStyle")) {
                properties._dashStyle = 1;
                switch (message.dashStyle) {
                default:
                    return "dashStyle: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                case 6:
                case 7:
                case 8:
                case 9:
                case 10:
                case 11:
                    break;
                }
            }
            if (message.lineWidth != null && message.hasOwnProperty("lineWidth")) {
                properties._lineWidth = 1;
                if (!$util.isInteger(message.lineWidth))
                    return "lineWidth: integer expected";
            }
            return null;
        };

        /**
         * Creates a Line message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.Line
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.Line} Line
         */
        Line.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.Line)
                return object;
            let message = new $root.epoch_proto.Line();
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.Line.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.Line.data: object expected");
                    message.data[i] = $root.epoch_proto.Point.fromObject(object.data[i]);
                }
            }
            if (object.name != null)
                message.name = String(object.name);
            switch (object.dashStyle) {
            default:
                if (typeof object.dashStyle === "number") {
                    message.dashStyle = object.dashStyle;
                    break;
                }
                break;
            case "DashStyleUnspecified":
            case 0:
                message.dashStyle = 0;
                break;
            case "Solid":
            case 1:
                message.dashStyle = 1;
                break;
            case "ShortDash":
            case 2:
                message.dashStyle = 2;
                break;
            case "ShortDot":
            case 3:
                message.dashStyle = 3;
                break;
            case "ShortDashDot":
            case 4:
                message.dashStyle = 4;
                break;
            case "ShortDashDotDot":
            case 5:
                message.dashStyle = 5;
                break;
            case "Dot":
            case 6:
                message.dashStyle = 6;
                break;
            case "Dash":
            case 7:
                message.dashStyle = 7;
                break;
            case "LongDash":
            case 8:
                message.dashStyle = 8;
                break;
            case "DashDot":
            case 9:
                message.dashStyle = 9;
                break;
            case "LongDashDot":
            case 10:
                message.dashStyle = 10;
                break;
            case "LongDashDotDot":
            case 11:
                message.dashStyle = 11;
                break;
            }
            if (object.lineWidth != null)
                message.lineWidth = object.lineWidth >>> 0;
            return message;
        };

        /**
         * Creates a plain object from a Line message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.Line
         * @static
         * @param {epoch_proto.Line} message Line
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Line.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.data = [];
            if (options.defaults)
                object.name = "";
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.Point.toObject(message.data[j], options);
            }
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.dashStyle != null && message.hasOwnProperty("dashStyle")) {
                object.dashStyle = options.enums === String ? $root.epoch_proto.DashStyle[message.dashStyle] === undefined ? message.dashStyle : $root.epoch_proto.DashStyle[message.dashStyle] : message.dashStyle;
                if (options.oneofs)
                    object._dashStyle = "dashStyle";
            }
            if (message.lineWidth != null && message.hasOwnProperty("lineWidth")) {
                object.lineWidth = message.lineWidth;
                if (options.oneofs)
                    object._lineWidth = "lineWidth";
            }
            return object;
        };

        /**
         * Converts this Line to JSON.
         * @function toJSON
         * @memberof epoch_proto.Line
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Line.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for Line
         * @function getTypeUrl
         * @memberof epoch_proto.Line
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        Line.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.Line";
        };

        return Line;
    })();

    epoch_proto.NumericLine = (function() {

        /**
         * Properties of a NumericLine.
         * @memberof epoch_proto
         * @interface INumericLine
         * @property {Array.<epoch_proto.INumericPoint>|null} [data] NumericLine data
         * @property {string|null} [name] NumericLine name
         * @property {epoch_proto.DashStyle|null} [dashStyle] NumericLine dashStyle
         * @property {number|null} [lineWidth] NumericLine lineWidth
         */

        /**
         * Constructs a new NumericLine.
         * @memberof epoch_proto
         * @classdesc Represents a NumericLine.
         * @implements INumericLine
         * @constructor
         * @param {epoch_proto.INumericLine=} [properties] Properties to set
         */
        function NumericLine(properties) {
            this.data = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NumericLine data.
         * @member {Array.<epoch_proto.INumericPoint>} data
         * @memberof epoch_proto.NumericLine
         * @instance
         */
        NumericLine.prototype.data = $util.emptyArray;

        /**
         * NumericLine name.
         * @member {string} name
         * @memberof epoch_proto.NumericLine
         * @instance
         */
        NumericLine.prototype.name = "";

        /**
         * NumericLine dashStyle.
         * @member {epoch_proto.DashStyle|null|undefined} dashStyle
         * @memberof epoch_proto.NumericLine
         * @instance
         */
        NumericLine.prototype.dashStyle = null;

        /**
         * NumericLine lineWidth.
         * @member {number|null|undefined} lineWidth
         * @memberof epoch_proto.NumericLine
         * @instance
         */
        NumericLine.prototype.lineWidth = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(NumericLine.prototype, "_dashStyle", {
            get: $util.oneOfGetter($oneOfFields = ["dashStyle"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(NumericLine.prototype, "_lineWidth", {
            get: $util.oneOfGetter($oneOfFields = ["lineWidth"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new NumericLine instance using the specified properties.
         * @function create
         * @memberof epoch_proto.NumericLine
         * @static
         * @param {epoch_proto.INumericLine=} [properties] Properties to set
         * @returns {epoch_proto.NumericLine} NumericLine instance
         */
        NumericLine.create = function create(properties) {
            return new NumericLine(properties);
        };

        /**
         * Encodes the specified NumericLine message. Does not implicitly {@link epoch_proto.NumericLine.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.NumericLine
         * @static
         * @param {epoch_proto.INumericLine} message NumericLine message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericLine.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.NumericPoint.encode(message.data[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.name);
            if (message.dashStyle != null && Object.hasOwnProperty.call(message, "dashStyle"))
                writer.uint32(/* id 3, wireType 0 =*/24).int32(message.dashStyle);
            if (message.lineWidth != null && Object.hasOwnProperty.call(message, "lineWidth"))
                writer.uint32(/* id 4, wireType 0 =*/32).uint32(message.lineWidth);
            return writer;
        };

        /**
         * Encodes the specified NumericLine message, length delimited. Does not implicitly {@link epoch_proto.NumericLine.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.NumericLine
         * @static
         * @param {epoch_proto.INumericLine} message NumericLine message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericLine.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NumericLine message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.NumericLine
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.NumericLine} NumericLine
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericLine.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.NumericLine();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.NumericPoint.decode(reader, reader.uint32()));
                        break;
                    }
                case 2: {
                        message.name = reader.string();
                        break;
                    }
                case 3: {
                        message.dashStyle = reader.int32();
                        break;
                    }
                case 4: {
                        message.lineWidth = reader.uint32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NumericLine message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.NumericLine
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.NumericLine} NumericLine
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericLine.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NumericLine message.
         * @function verify
         * @memberof epoch_proto.NumericLine
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NumericLine.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.NumericPoint.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.dashStyle != null && message.hasOwnProperty("dashStyle")) {
                properties._dashStyle = 1;
                switch (message.dashStyle) {
                default:
                    return "dashStyle: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                case 6:
                case 7:
                case 8:
                case 9:
                case 10:
                case 11:
                    break;
                }
            }
            if (message.lineWidth != null && message.hasOwnProperty("lineWidth")) {
                properties._lineWidth = 1;
                if (!$util.isInteger(message.lineWidth))
                    return "lineWidth: integer expected";
            }
            return null;
        };

        /**
         * Creates a NumericLine message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.NumericLine
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.NumericLine} NumericLine
         */
        NumericLine.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.NumericLine)
                return object;
            let message = new $root.epoch_proto.NumericLine();
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.NumericLine.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.NumericLine.data: object expected");
                    message.data[i] = $root.epoch_proto.NumericPoint.fromObject(object.data[i]);
                }
            }
            if (object.name != null)
                message.name = String(object.name);
            switch (object.dashStyle) {
            default:
                if (typeof object.dashStyle === "number") {
                    message.dashStyle = object.dashStyle;
                    break;
                }
                break;
            case "DashStyleUnspecified":
            case 0:
                message.dashStyle = 0;
                break;
            case "Solid":
            case 1:
                message.dashStyle = 1;
                break;
            case "ShortDash":
            case 2:
                message.dashStyle = 2;
                break;
            case "ShortDot":
            case 3:
                message.dashStyle = 3;
                break;
            case "ShortDashDot":
            case 4:
                message.dashStyle = 4;
                break;
            case "ShortDashDotDot":
            case 5:
                message.dashStyle = 5;
                break;
            case "Dot":
            case 6:
                message.dashStyle = 6;
                break;
            case "Dash":
            case 7:
                message.dashStyle = 7;
                break;
            case "LongDash":
            case 8:
                message.dashStyle = 8;
                break;
            case "DashDot":
            case 9:
                message.dashStyle = 9;
                break;
            case "LongDashDot":
            case 10:
                message.dashStyle = 10;
                break;
            case "LongDashDotDot":
            case 11:
                message.dashStyle = 11;
                break;
            }
            if (object.lineWidth != null)
                message.lineWidth = object.lineWidth >>> 0;
            return message;
        };

        /**
         * Creates a plain object from a NumericLine message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.NumericLine
         * @static
         * @param {epoch_proto.NumericLine} message NumericLine
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NumericLine.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.data = [];
            if (options.defaults)
                object.name = "";
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.NumericPoint.toObject(message.data[j], options);
            }
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.dashStyle != null && message.hasOwnProperty("dashStyle")) {
                object.dashStyle = options.enums === String ? $root.epoch_proto.DashStyle[message.dashStyle] === undefined ? message.dashStyle : $root.epoch_proto.DashStyle[message.dashStyle] : message.dashStyle;
                if (options.oneofs)
                    object._dashStyle = "dashStyle";
            }
            if (message.lineWidth != null && message.hasOwnProperty("lineWidth")) {
                object.lineWidth = message.lineWidth;
                if (options.oneofs)
                    object._lineWidth = "lineWidth";
            }
            return object;
        };

        /**
         * Converts this NumericLine to JSON.
         * @function toJSON
         * @memberof epoch_proto.NumericLine
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NumericLine.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NumericLine
         * @function getTypeUrl
         * @memberof epoch_proto.NumericLine
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NumericLine.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.NumericLine";
        };

        return NumericLine;
    })();

    /**
     * StackType enum.
     * @name epoch_proto.StackType
     * @enum {number}
     * @property {number} StackTypeUnspecified=0 StackTypeUnspecified value
     * @property {number} StackTypeNormal=1 StackTypeNormal value
     * @property {number} StackTypePercent=2 StackTypePercent value
     */
    epoch_proto.StackType = (function() {
        const valuesById = {}, values = Object.create(valuesById);
        values[valuesById[0] = "StackTypeUnspecified"] = 0;
        values[valuesById[1] = "StackTypeNormal"] = 1;
        values[valuesById[2] = "StackTypePercent"] = 2;
        return values;
    })();

    epoch_proto.ColumnDef = (function() {

        /**
         * Properties of a ColumnDef.
         * @memberof epoch_proto
         * @interface IColumnDef
         * @property {string|null} [id] ColumnDef id
         * @property {string|null} [name] ColumnDef name
         * @property {epoch_proto.EpochFolioType|null} [type] ColumnDef type
         * @property {number|null} [decimalPlaces] ColumnDef decimalPlaces
         */

        /**
         * Constructs a new ColumnDef.
         * @memberof epoch_proto
         * @classdesc Represents a ColumnDef.
         * @implements IColumnDef
         * @constructor
         * @param {epoch_proto.IColumnDef=} [properties] Properties to set
         */
        function ColumnDef(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ColumnDef id.
         * @member {string} id
         * @memberof epoch_proto.ColumnDef
         * @instance
         */
        ColumnDef.prototype.id = "";

        /**
         * ColumnDef name.
         * @member {string} name
         * @memberof epoch_proto.ColumnDef
         * @instance
         */
        ColumnDef.prototype.name = "";

        /**
         * ColumnDef type.
         * @member {epoch_proto.EpochFolioType} type
         * @memberof epoch_proto.ColumnDef
         * @instance
         */
        ColumnDef.prototype.type = 0;

        /**
         * ColumnDef decimalPlaces.
         * @member {number|null|undefined} decimalPlaces
         * @memberof epoch_proto.ColumnDef
         * @instance
         */
        ColumnDef.prototype.decimalPlaces = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(ColumnDef.prototype, "_decimalPlaces", {
            get: $util.oneOfGetter($oneOfFields = ["decimalPlaces"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new ColumnDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.ColumnDef
         * @static
         * @param {epoch_proto.IColumnDef=} [properties] Properties to set
         * @returns {epoch_proto.ColumnDef} ColumnDef instance
         */
        ColumnDef.create = function create(properties) {
            return new ColumnDef(properties);
        };

        /**
         * Encodes the specified ColumnDef message. Does not implicitly {@link epoch_proto.ColumnDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.ColumnDef
         * @static
         * @param {epoch_proto.IColumnDef} message ColumnDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ColumnDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.name);
            if (message.type != null && Object.hasOwnProperty.call(message, "type"))
                writer.uint32(/* id 3, wireType 0 =*/24).int32(message.type);
            if (message.decimalPlaces != null && Object.hasOwnProperty.call(message, "decimalPlaces"))
                writer.uint32(/* id 4, wireType 0 =*/32).int32(message.decimalPlaces);
            return writer;
        };

        /**
         * Encodes the specified ColumnDef message, length delimited. Does not implicitly {@link epoch_proto.ColumnDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.ColumnDef
         * @static
         * @param {epoch_proto.IColumnDef} message ColumnDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ColumnDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ColumnDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.ColumnDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.ColumnDef} ColumnDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ColumnDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.ColumnDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.name = reader.string();
                        break;
                    }
                case 3: {
                        message.type = reader.int32();
                        break;
                    }
                case 4: {
                        message.decimalPlaces = reader.int32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ColumnDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.ColumnDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.ColumnDef} ColumnDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ColumnDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ColumnDef message.
         * @function verify
         * @memberof epoch_proto.ColumnDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ColumnDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.type != null && message.hasOwnProperty("type"))
                switch (message.type) {
                default:
                    return "type: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                case 6:
                case 7:
                case 8:
                case 9:
                case 10:
                    break;
                }
            if (message.decimalPlaces != null && message.hasOwnProperty("decimalPlaces")) {
                properties._decimalPlaces = 1;
                if (!$util.isInteger(message.decimalPlaces))
                    return "decimalPlaces: integer expected";
            }
            return null;
        };

        /**
         * Creates a ColumnDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.ColumnDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.ColumnDef} ColumnDef
         */
        ColumnDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.ColumnDef)
                return object;
            let message = new $root.epoch_proto.ColumnDef();
            if (object.id != null)
                message.id = String(object.id);
            if (object.name != null)
                message.name = String(object.name);
            switch (object.type) {
            default:
                if (typeof object.type === "number") {
                    message.type = object.type;
                    break;
                }
                break;
            case "TypeUnspecified":
            case 0:
                message.type = 0;
                break;
            case "TypeString":
            case 1:
                message.type = 1;
                break;
            case "TypeInteger":
            case 2:
                message.type = 2;
                break;
            case "TypeDecimal":
            case 3:
                message.type = 3;
                break;
            case "TypePercent":
            case 4:
                message.type = 4;
                break;
            case "TypeBoolean":
            case 5:
                message.type = 5;
                break;
            case "TypeDateTime":
            case 6:
                message.type = 6;
                break;
            case "TypeDate":
            case 7:
                message.type = 7;
                break;
            case "TypeDayDuration":
            case 8:
                message.type = 8;
                break;
            case "TypeMonetary":
            case 9:
                message.type = 9;
                break;
            case "TypeDuration":
            case 10:
                message.type = 10;
                break;
            }
            if (object.decimalPlaces != null)
                message.decimalPlaces = object.decimalPlaces | 0;
            return message;
        };

        /**
         * Creates a plain object from a ColumnDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.ColumnDef
         * @static
         * @param {epoch_proto.ColumnDef} message ColumnDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ColumnDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.id = "";
                object.name = "";
                object.type = options.enums === String ? "TypeUnspecified" : 0;
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.type != null && message.hasOwnProperty("type"))
                object.type = options.enums === String ? $root.epoch_proto.EpochFolioType[message.type] === undefined ? message.type : $root.epoch_proto.EpochFolioType[message.type] : message.type;
            if (message.decimalPlaces != null && message.hasOwnProperty("decimalPlaces")) {
                object.decimalPlaces = message.decimalPlaces;
                if (options.oneofs)
                    object._decimalPlaces = "decimalPlaces";
            }
            return object;
        };

        /**
         * Converts this ColumnDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.ColumnDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ColumnDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ColumnDef
         * @function getTypeUrl
         * @memberof epoch_proto.ColumnDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ColumnDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.ColumnDef";
        };

        return ColumnDef;
    })();

    epoch_proto.TableRow = (function() {

        /**
         * Properties of a TableRow.
         * @memberof epoch_proto
         * @interface ITableRow
         * @property {Array.<epoch_proto.IScalar>|null} [values] TableRow values
         */

        /**
         * Constructs a new TableRow.
         * @memberof epoch_proto
         * @classdesc Represents a TableRow.
         * @implements ITableRow
         * @constructor
         * @param {epoch_proto.ITableRow=} [properties] Properties to set
         */
        function TableRow(properties) {
            this.values = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * TableRow values.
         * @member {Array.<epoch_proto.IScalar>} values
         * @memberof epoch_proto.TableRow
         * @instance
         */
        TableRow.prototype.values = $util.emptyArray;

        /**
         * Creates a new TableRow instance using the specified properties.
         * @function create
         * @memberof epoch_proto.TableRow
         * @static
         * @param {epoch_proto.ITableRow=} [properties] Properties to set
         * @returns {epoch_proto.TableRow} TableRow instance
         */
        TableRow.create = function create(properties) {
            return new TableRow(properties);
        };

        /**
         * Encodes the specified TableRow message. Does not implicitly {@link epoch_proto.TableRow.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.TableRow
         * @static
         * @param {epoch_proto.ITableRow} message TableRow message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TableRow.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.values != null && message.values.length)
                for (let i = 0; i < message.values.length; ++i)
                    $root.epoch_proto.Scalar.encode(message.values[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified TableRow message, length delimited. Does not implicitly {@link epoch_proto.TableRow.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.TableRow
         * @static
         * @param {epoch_proto.ITableRow} message TableRow message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TableRow.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a TableRow message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.TableRow
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.TableRow} TableRow
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TableRow.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.TableRow();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.values && message.values.length))
                            message.values = [];
                        message.values.push($root.epoch_proto.Scalar.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a TableRow message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.TableRow
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.TableRow} TableRow
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TableRow.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a TableRow message.
         * @function verify
         * @memberof epoch_proto.TableRow
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        TableRow.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.values != null && message.hasOwnProperty("values")) {
                if (!Array.isArray(message.values))
                    return "values: array expected";
                for (let i = 0; i < message.values.length; ++i) {
                    let error = $root.epoch_proto.Scalar.verify(message.values[i]);
                    if (error)
                        return "values." + error;
                }
            }
            return null;
        };

        /**
         * Creates a TableRow message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.TableRow
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.TableRow} TableRow
         */
        TableRow.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.TableRow)
                return object;
            let message = new $root.epoch_proto.TableRow();
            if (object.values) {
                if (!Array.isArray(object.values))
                    throw TypeError(".epoch_proto.TableRow.values: array expected");
                message.values = [];
                for (let i = 0; i < object.values.length; ++i) {
                    if (typeof object.values[i] !== "object")
                        throw TypeError(".epoch_proto.TableRow.values: object expected");
                    message.values[i] = $root.epoch_proto.Scalar.fromObject(object.values[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a TableRow message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.TableRow
         * @static
         * @param {epoch_proto.TableRow} message TableRow
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        TableRow.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.values = [];
            if (message.values && message.values.length) {
                object.values = [];
                for (let j = 0; j < message.values.length; ++j)
                    object.values[j] = $root.epoch_proto.Scalar.toObject(message.values[j], options);
            }
            return object;
        };

        /**
         * Converts this TableRow to JSON.
         * @function toJSON
         * @memberof epoch_proto.TableRow
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        TableRow.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for TableRow
         * @function getTypeUrl
         * @memberof epoch_proto.TableRow
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        TableRow.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.TableRow";
        };

        return TableRow;
    })();

    epoch_proto.TableData = (function() {

        /**
         * Properties of a TableData.
         * @memberof epoch_proto
         * @interface ITableData
         * @property {Array.<epoch_proto.ITableRow>|null} [rows] TableData rows
         */

        /**
         * Constructs a new TableData.
         * @memberof epoch_proto
         * @classdesc Represents a TableData.
         * @implements ITableData
         * @constructor
         * @param {epoch_proto.ITableData=} [properties] Properties to set
         */
        function TableData(properties) {
            this.rows = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * TableData rows.
         * @member {Array.<epoch_proto.ITableRow>} rows
         * @memberof epoch_proto.TableData
         * @instance
         */
        TableData.prototype.rows = $util.emptyArray;

        /**
         * Creates a new TableData instance using the specified properties.
         * @function create
         * @memberof epoch_proto.TableData
         * @static
         * @param {epoch_proto.ITableData=} [properties] Properties to set
         * @returns {epoch_proto.TableData} TableData instance
         */
        TableData.create = function create(properties) {
            return new TableData(properties);
        };

        /**
         * Encodes the specified TableData message. Does not implicitly {@link epoch_proto.TableData.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.TableData
         * @static
         * @param {epoch_proto.ITableData} message TableData message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TableData.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.rows != null && message.rows.length)
                for (let i = 0; i < message.rows.length; ++i)
                    $root.epoch_proto.TableRow.encode(message.rows[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified TableData message, length delimited. Does not implicitly {@link epoch_proto.TableData.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.TableData
         * @static
         * @param {epoch_proto.ITableData} message TableData message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TableData.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a TableData message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.TableData
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.TableData} TableData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TableData.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.TableData();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.rows && message.rows.length))
                            message.rows = [];
                        message.rows.push($root.epoch_proto.TableRow.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a TableData message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.TableData
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.TableData} TableData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TableData.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a TableData message.
         * @function verify
         * @memberof epoch_proto.TableData
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        TableData.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.rows != null && message.hasOwnProperty("rows")) {
                if (!Array.isArray(message.rows))
                    return "rows: array expected";
                for (let i = 0; i < message.rows.length; ++i) {
                    let error = $root.epoch_proto.TableRow.verify(message.rows[i]);
                    if (error)
                        return "rows." + error;
                }
            }
            return null;
        };

        /**
         * Creates a TableData message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.TableData
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.TableData} TableData
         */
        TableData.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.TableData)
                return object;
            let message = new $root.epoch_proto.TableData();
            if (object.rows) {
                if (!Array.isArray(object.rows))
                    throw TypeError(".epoch_proto.TableData.rows: array expected");
                message.rows = [];
                for (let i = 0; i < object.rows.length; ++i) {
                    if (typeof object.rows[i] !== "object")
                        throw TypeError(".epoch_proto.TableData.rows: object expected");
                    message.rows[i] = $root.epoch_proto.TableRow.fromObject(object.rows[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a TableData message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.TableData
         * @static
         * @param {epoch_proto.TableData} message TableData
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        TableData.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.rows = [];
            if (message.rows && message.rows.length) {
                object.rows = [];
                for (let j = 0; j < message.rows.length; ++j)
                    object.rows[j] = $root.epoch_proto.TableRow.toObject(message.rows[j], options);
            }
            return object;
        };

        /**
         * Converts this TableData to JSON.
         * @function toJSON
         * @memberof epoch_proto.TableData
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        TableData.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for TableData
         * @function getTypeUrl
         * @memberof epoch_proto.TableData
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        TableData.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.TableData";
        };

        return TableData;
    })();

    epoch_proto.Table = (function() {

        /**
         * Properties of a Table.
         * @memberof epoch_proto
         * @interface ITable
         * @property {epoch_proto.EpochFolioDashboardWidget|null} [type] Table type
         * @property {string|null} [category] Table category
         * @property {string|null} [title] Table title
         * @property {Array.<epoch_proto.IColumnDef>|null} [columns] Table columns
         * @property {epoch_proto.ITableData|null} [data] Table data
         */

        /**
         * Constructs a new Table.
         * @memberof epoch_proto
         * @classdesc Represents a Table.
         * @implements ITable
         * @constructor
         * @param {epoch_proto.ITable=} [properties] Properties to set
         */
        function Table(properties) {
            this.columns = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Table type.
         * @member {epoch_proto.EpochFolioDashboardWidget} type
         * @memberof epoch_proto.Table
         * @instance
         */
        Table.prototype.type = 0;

        /**
         * Table category.
         * @member {string} category
         * @memberof epoch_proto.Table
         * @instance
         */
        Table.prototype.category = "";

        /**
         * Table title.
         * @member {string} title
         * @memberof epoch_proto.Table
         * @instance
         */
        Table.prototype.title = "";

        /**
         * Table columns.
         * @member {Array.<epoch_proto.IColumnDef>} columns
         * @memberof epoch_proto.Table
         * @instance
         */
        Table.prototype.columns = $util.emptyArray;

        /**
         * Table data.
         * @member {epoch_proto.ITableData|null|undefined} data
         * @memberof epoch_proto.Table
         * @instance
         */
        Table.prototype.data = null;

        /**
         * Creates a new Table instance using the specified properties.
         * @function create
         * @memberof epoch_proto.Table
         * @static
         * @param {epoch_proto.ITable=} [properties] Properties to set
         * @returns {epoch_proto.Table} Table instance
         */
        Table.create = function create(properties) {
            return new Table(properties);
        };

        /**
         * Encodes the specified Table message. Does not implicitly {@link epoch_proto.Table.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.Table
         * @static
         * @param {epoch_proto.ITable} message Table message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Table.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.type != null && Object.hasOwnProperty.call(message, "type"))
                writer.uint32(/* id 1, wireType 0 =*/8).int32(message.type);
            if (message.category != null && Object.hasOwnProperty.call(message, "category"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.category);
            if (message.title != null && Object.hasOwnProperty.call(message, "title"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.title);
            if (message.columns != null && message.columns.length)
                for (let i = 0; i < message.columns.length; ++i)
                    $root.epoch_proto.ColumnDef.encode(message.columns[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
            if (message.data != null && Object.hasOwnProperty.call(message, "data"))
                $root.epoch_proto.TableData.encode(message.data, writer.uint32(/* id 5, wireType 2 =*/42).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified Table message, length delimited. Does not implicitly {@link epoch_proto.Table.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.Table
         * @static
         * @param {epoch_proto.ITable} message Table message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Table.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a Table message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.Table
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.Table} Table
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Table.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.Table();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.type = reader.int32();
                        break;
                    }
                case 2: {
                        message.category = reader.string();
                        break;
                    }
                case 3: {
                        message.title = reader.string();
                        break;
                    }
                case 4: {
                        if (!(message.columns && message.columns.length))
                            message.columns = [];
                        message.columns.push($root.epoch_proto.ColumnDef.decode(reader, reader.uint32()));
                        break;
                    }
                case 5: {
                        message.data = $root.epoch_proto.TableData.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a Table message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.Table
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.Table} Table
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Table.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a Table message.
         * @function verify
         * @memberof epoch_proto.Table
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Table.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.type != null && message.hasOwnProperty("type"))
                switch (message.type) {
                default:
                    return "type: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                case 6:
                case 7:
                case 8:
                case 9:
                case 10:
                case 11:
                case 12:
                case 13:
                case 14:
                case 15:
                case 16:
                case 17:
                case 18:
                case 19:
                case 20:
                case 21:
                case 22:
                case 23:
                case 24:
                    break;
                }
            if (message.category != null && message.hasOwnProperty("category"))
                if (!$util.isString(message.category))
                    return "category: string expected";
            if (message.title != null && message.hasOwnProperty("title"))
                if (!$util.isString(message.title))
                    return "title: string expected";
            if (message.columns != null && message.hasOwnProperty("columns")) {
                if (!Array.isArray(message.columns))
                    return "columns: array expected";
                for (let i = 0; i < message.columns.length; ++i) {
                    let error = $root.epoch_proto.ColumnDef.verify(message.columns[i]);
                    if (error)
                        return "columns." + error;
                }
            }
            if (message.data != null && message.hasOwnProperty("data")) {
                let error = $root.epoch_proto.TableData.verify(message.data);
                if (error)
                    return "data." + error;
            }
            return null;
        };

        /**
         * Creates a Table message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.Table
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.Table} Table
         */
        Table.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.Table)
                return object;
            let message = new $root.epoch_proto.Table();
            switch (object.type) {
            default:
                if (typeof object.type === "number") {
                    message.type = object.type;
                    break;
                }
                break;
            case "WidgetUnspecified":
            case 0:
                message.type = 0;
                break;
            case "WidgetCard":
            case 1:
                message.type = 1;
                break;
            case "WidgetLines":
            case 2:
                message.type = 2;
                break;
            case "WidgetBar":
            case 3:
                message.type = 3;
                break;
            case "WidgetDataTable":
            case 4:
                message.type = 4;
                break;
            case "WidgetXRange":
            case 5:
                message.type = 5;
                break;
            case "WidgetHistogram":
            case 6:
                message.type = 6;
                break;
            case "WidgetPie":
            case 7:
                message.type = 7;
                break;
            case "WidgetHeatMap":
            case 8:
                message.type = 8;
                break;
            case "WidgetBoxPlot":
            case 9:
                message.type = 9;
                break;
            case "WidgetArea":
            case 10:
                message.type = 10;
                break;
            case "WidgetColumn":
            case 11:
                message.type = 11;
                break;
            case "WidgetScatter":
            case 12:
                message.type = 12;
                break;
            case "WidgetWaterfall":
            case 13:
                message.type = 13;
                break;
            case "WidgetSpline":
            case 14:
                message.type = 14;
                break;
            case "WidgetBubble":
            case 15:
                message.type = 15;
                break;
            case "WidgetTreemap":
            case 16:
                message.type = 16;
                break;
            case "WidgetSankey":
            case 17:
                message.type = 17;
                break;
            case "WidgetAreaRange":
            case 18:
                message.type = 18;
                break;
            case "WidgetGauge":
            case 19:
                message.type = 19;
                break;
            case "WidgetBullet":
            case 20:
                message.type = 20;
                break;
            case "WidgetTimeline":
            case 21:
                message.type = 21;
                break;
            case "WidgetErrorBar":
            case 22:
                message.type = 22;
                break;
            case "WidgetBellCurve":
            case 23:
                message.type = 23;
                break;
            case "WidgetNumericErrorBar":
            case 24:
                message.type = 24;
                break;
            }
            if (object.category != null)
                message.category = String(object.category);
            if (object.title != null)
                message.title = String(object.title);
            if (object.columns) {
                if (!Array.isArray(object.columns))
                    throw TypeError(".epoch_proto.Table.columns: array expected");
                message.columns = [];
                for (let i = 0; i < object.columns.length; ++i) {
                    if (typeof object.columns[i] !== "object")
                        throw TypeError(".epoch_proto.Table.columns: object expected");
                    message.columns[i] = $root.epoch_proto.ColumnDef.fromObject(object.columns[i]);
                }
            }
            if (object.data != null) {
                if (typeof object.data !== "object")
                    throw TypeError(".epoch_proto.Table.data: object expected");
                message.data = $root.epoch_proto.TableData.fromObject(object.data);
            }
            return message;
        };

        /**
         * Creates a plain object from a Table message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.Table
         * @static
         * @param {epoch_proto.Table} message Table
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Table.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.columns = [];
            if (options.defaults) {
                object.type = options.enums === String ? "WidgetUnspecified" : 0;
                object.category = "";
                object.title = "";
                object.data = null;
            }
            if (message.type != null && message.hasOwnProperty("type"))
                object.type = options.enums === String ? $root.epoch_proto.EpochFolioDashboardWidget[message.type] === undefined ? message.type : $root.epoch_proto.EpochFolioDashboardWidget[message.type] : message.type;
            if (message.category != null && message.hasOwnProperty("category"))
                object.category = message.category;
            if (message.title != null && message.hasOwnProperty("title"))
                object.title = message.title;
            if (message.columns && message.columns.length) {
                object.columns = [];
                for (let j = 0; j < message.columns.length; ++j)
                    object.columns[j] = $root.epoch_proto.ColumnDef.toObject(message.columns[j], options);
            }
            if (message.data != null && message.hasOwnProperty("data"))
                object.data = $root.epoch_proto.TableData.toObject(message.data, options);
            return object;
        };

        /**
         * Converts this Table to JSON.
         * @function toJSON
         * @memberof epoch_proto.Table
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Table.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for Table
         * @function getTypeUrl
         * @memberof epoch_proto.Table
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        Table.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.Table";
        };

        return Table;
    })();

    epoch_proto.CardData = (function() {

        /**
         * Properties of a CardData.
         * @memberof epoch_proto
         * @interface ICardData
         * @property {string|null} [title] CardData title
         * @property {epoch_proto.IScalar|null} [value] CardData value
         * @property {epoch_proto.EpochFolioType|null} [type] CardData type
         * @property {number|Long|null} [group] CardData group
         * @property {number|null} [decimalPlaces] CardData decimalPlaces
         */

        /**
         * Constructs a new CardData.
         * @memberof epoch_proto
         * @classdesc Represents a CardData.
         * @implements ICardData
         * @constructor
         * @param {epoch_proto.ICardData=} [properties] Properties to set
         */
        function CardData(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CardData title.
         * @member {string} title
         * @memberof epoch_proto.CardData
         * @instance
         */
        CardData.prototype.title = "";

        /**
         * CardData value.
         * @member {epoch_proto.IScalar|null|undefined} value
         * @memberof epoch_proto.CardData
         * @instance
         */
        CardData.prototype.value = null;

        /**
         * CardData type.
         * @member {epoch_proto.EpochFolioType} type
         * @memberof epoch_proto.CardData
         * @instance
         */
        CardData.prototype.type = 0;

        /**
         * CardData group.
         * @member {number|Long} group
         * @memberof epoch_proto.CardData
         * @instance
         */
        CardData.prototype.group = $util.Long ? $util.Long.fromBits(0,0,true) : 0;

        /**
         * CardData decimalPlaces.
         * @member {number|null|undefined} decimalPlaces
         * @memberof epoch_proto.CardData
         * @instance
         */
        CardData.prototype.decimalPlaces = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(CardData.prototype, "_decimalPlaces", {
            get: $util.oneOfGetter($oneOfFields = ["decimalPlaces"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new CardData instance using the specified properties.
         * @function create
         * @memberof epoch_proto.CardData
         * @static
         * @param {epoch_proto.ICardData=} [properties] Properties to set
         * @returns {epoch_proto.CardData} CardData instance
         */
        CardData.create = function create(properties) {
            return new CardData(properties);
        };

        /**
         * Encodes the specified CardData message. Does not implicitly {@link epoch_proto.CardData.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.CardData
         * @static
         * @param {epoch_proto.ICardData} message CardData message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CardData.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.title != null && Object.hasOwnProperty.call(message, "title"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.title);
            if (message.value != null && Object.hasOwnProperty.call(message, "value"))
                $root.epoch_proto.Scalar.encode(message.value, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.type != null && Object.hasOwnProperty.call(message, "type"))
                writer.uint32(/* id 3, wireType 0 =*/24).int32(message.type);
            if (message.group != null && Object.hasOwnProperty.call(message, "group"))
                writer.uint32(/* id 4, wireType 0 =*/32).uint64(message.group);
            if (message.decimalPlaces != null && Object.hasOwnProperty.call(message, "decimalPlaces"))
                writer.uint32(/* id 5, wireType 0 =*/40).int32(message.decimalPlaces);
            return writer;
        };

        /**
         * Encodes the specified CardData message, length delimited. Does not implicitly {@link epoch_proto.CardData.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.CardData
         * @static
         * @param {epoch_proto.ICardData} message CardData message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CardData.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CardData message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.CardData
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.CardData} CardData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CardData.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.CardData();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.title = reader.string();
                        break;
                    }
                case 2: {
                        message.value = $root.epoch_proto.Scalar.decode(reader, reader.uint32());
                        break;
                    }
                case 3: {
                        message.type = reader.int32();
                        break;
                    }
                case 4: {
                        message.group = reader.uint64();
                        break;
                    }
                case 5: {
                        message.decimalPlaces = reader.int32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CardData message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.CardData
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.CardData} CardData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CardData.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CardData message.
         * @function verify
         * @memberof epoch_proto.CardData
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CardData.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.title != null && message.hasOwnProperty("title"))
                if (!$util.isString(message.title))
                    return "title: string expected";
            if (message.value != null && message.hasOwnProperty("value")) {
                let error = $root.epoch_proto.Scalar.verify(message.value);
                if (error)
                    return "value." + error;
            }
            if (message.type != null && message.hasOwnProperty("type"))
                switch (message.type) {
                default:
                    return "type: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                case 6:
                case 7:
                case 8:
                case 9:
                case 10:
                    break;
                }
            if (message.group != null && message.hasOwnProperty("group"))
                if (!$util.isInteger(message.group) && !(message.group && $util.isInteger(message.group.low) && $util.isInteger(message.group.high)))
                    return "group: integer|Long expected";
            if (message.decimalPlaces != null && message.hasOwnProperty("decimalPlaces")) {
                properties._decimalPlaces = 1;
                if (!$util.isInteger(message.decimalPlaces))
                    return "decimalPlaces: integer expected";
            }
            return null;
        };

        /**
         * Creates a CardData message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.CardData
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.CardData} CardData
         */
        CardData.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.CardData)
                return object;
            let message = new $root.epoch_proto.CardData();
            if (object.title != null)
                message.title = String(object.title);
            if (object.value != null) {
                if (typeof object.value !== "object")
                    throw TypeError(".epoch_proto.CardData.value: object expected");
                message.value = $root.epoch_proto.Scalar.fromObject(object.value);
            }
            switch (object.type) {
            default:
                if (typeof object.type === "number") {
                    message.type = object.type;
                    break;
                }
                break;
            case "TypeUnspecified":
            case 0:
                message.type = 0;
                break;
            case "TypeString":
            case 1:
                message.type = 1;
                break;
            case "TypeInteger":
            case 2:
                message.type = 2;
                break;
            case "TypeDecimal":
            case 3:
                message.type = 3;
                break;
            case "TypePercent":
            case 4:
                message.type = 4;
                break;
            case "TypeBoolean":
            case 5:
                message.type = 5;
                break;
            case "TypeDateTime":
            case 6:
                message.type = 6;
                break;
            case "TypeDate":
            case 7:
                message.type = 7;
                break;
            case "TypeDayDuration":
            case 8:
                message.type = 8;
                break;
            case "TypeMonetary":
            case 9:
                message.type = 9;
                break;
            case "TypeDuration":
            case 10:
                message.type = 10;
                break;
            }
            if (object.group != null)
                if ($util.Long)
                    (message.group = $util.Long.fromValue(object.group)).unsigned = true;
                else if (typeof object.group === "string")
                    message.group = parseInt(object.group, 10);
                else if (typeof object.group === "number")
                    message.group = object.group;
                else if (typeof object.group === "object")
                    message.group = new $util.LongBits(object.group.low >>> 0, object.group.high >>> 0).toNumber(true);
            if (object.decimalPlaces != null)
                message.decimalPlaces = object.decimalPlaces | 0;
            return message;
        };

        /**
         * Creates a plain object from a CardData message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.CardData
         * @static
         * @param {epoch_proto.CardData} message CardData
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CardData.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.title = "";
                object.value = null;
                object.type = options.enums === String ? "TypeUnspecified" : 0;
                if ($util.Long) {
                    let long = new $util.Long(0, 0, true);
                    object.group = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.group = options.longs === String ? "0" : 0;
            }
            if (message.title != null && message.hasOwnProperty("title"))
                object.title = message.title;
            if (message.value != null && message.hasOwnProperty("value"))
                object.value = $root.epoch_proto.Scalar.toObject(message.value, options);
            if (message.type != null && message.hasOwnProperty("type"))
                object.type = options.enums === String ? $root.epoch_proto.EpochFolioType[message.type] === undefined ? message.type : $root.epoch_proto.EpochFolioType[message.type] : message.type;
            if (message.group != null && message.hasOwnProperty("group"))
                if (typeof message.group === "number")
                    object.group = options.longs === String ? String(message.group) : message.group;
                else
                    object.group = options.longs === String ? $util.Long.prototype.toString.call(message.group) : options.longs === Number ? new $util.LongBits(message.group.low >>> 0, message.group.high >>> 0).toNumber(true) : message.group;
            if (message.decimalPlaces != null && message.hasOwnProperty("decimalPlaces")) {
                object.decimalPlaces = message.decimalPlaces;
                if (options.oneofs)
                    object._decimalPlaces = "decimalPlaces";
            }
            return object;
        };

        /**
         * Converts this CardData to JSON.
         * @function toJSON
         * @memberof epoch_proto.CardData
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CardData.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CardData
         * @function getTypeUrl
         * @memberof epoch_proto.CardData
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CardData.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.CardData";
        };

        return CardData;
    })();

    epoch_proto.CardDef = (function() {

        /**
         * Properties of a CardDef.
         * @memberof epoch_proto
         * @interface ICardDef
         * @property {epoch_proto.EpochFolioDashboardWidget|null} [type] CardDef type
         * @property {string|null} [category] CardDef category
         * @property {Array.<epoch_proto.ICardData>|null} [data] CardDef data
         * @property {number|Long|null} [groupSize] CardDef groupSize
         */

        /**
         * Constructs a new CardDef.
         * @memberof epoch_proto
         * @classdesc Represents a CardDef.
         * @implements ICardDef
         * @constructor
         * @param {epoch_proto.ICardDef=} [properties] Properties to set
         */
        function CardDef(properties) {
            this.data = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CardDef type.
         * @member {epoch_proto.EpochFolioDashboardWidget} type
         * @memberof epoch_proto.CardDef
         * @instance
         */
        CardDef.prototype.type = 0;

        /**
         * CardDef category.
         * @member {string} category
         * @memberof epoch_proto.CardDef
         * @instance
         */
        CardDef.prototype.category = "";

        /**
         * CardDef data.
         * @member {Array.<epoch_proto.ICardData>} data
         * @memberof epoch_proto.CardDef
         * @instance
         */
        CardDef.prototype.data = $util.emptyArray;

        /**
         * CardDef groupSize.
         * @member {number|Long} groupSize
         * @memberof epoch_proto.CardDef
         * @instance
         */
        CardDef.prototype.groupSize = $util.Long ? $util.Long.fromBits(0,0,true) : 0;

        /**
         * Creates a new CardDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.CardDef
         * @static
         * @param {epoch_proto.ICardDef=} [properties] Properties to set
         * @returns {epoch_proto.CardDef} CardDef instance
         */
        CardDef.create = function create(properties) {
            return new CardDef(properties);
        };

        /**
         * Encodes the specified CardDef message. Does not implicitly {@link epoch_proto.CardDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.CardDef
         * @static
         * @param {epoch_proto.ICardDef} message CardDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CardDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.type != null && Object.hasOwnProperty.call(message, "type"))
                writer.uint32(/* id 1, wireType 0 =*/8).int32(message.type);
            if (message.category != null && Object.hasOwnProperty.call(message, "category"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.category);
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.CardData.encode(message.data[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.groupSize != null && Object.hasOwnProperty.call(message, "groupSize"))
                writer.uint32(/* id 4, wireType 0 =*/32).uint64(message.groupSize);
            return writer;
        };

        /**
         * Encodes the specified CardDef message, length delimited. Does not implicitly {@link epoch_proto.CardDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.CardDef
         * @static
         * @param {epoch_proto.ICardDef} message CardDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CardDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CardDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.CardDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.CardDef} CardDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CardDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.CardDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.type = reader.int32();
                        break;
                    }
                case 2: {
                        message.category = reader.string();
                        break;
                    }
                case 3: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.CardData.decode(reader, reader.uint32()));
                        break;
                    }
                case 4: {
                        message.groupSize = reader.uint64();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CardDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.CardDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.CardDef} CardDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CardDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CardDef message.
         * @function verify
         * @memberof epoch_proto.CardDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CardDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.type != null && message.hasOwnProperty("type"))
                switch (message.type) {
                default:
                    return "type: enum value expected";
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                case 6:
                case 7:
                case 8:
                case 9:
                case 10:
                case 11:
                case 12:
                case 13:
                case 14:
                case 15:
                case 16:
                case 17:
                case 18:
                case 19:
                case 20:
                case 21:
                case 22:
                case 23:
                case 24:
                    break;
                }
            if (message.category != null && message.hasOwnProperty("category"))
                if (!$util.isString(message.category))
                    return "category: string expected";
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.CardData.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            if (message.groupSize != null && message.hasOwnProperty("groupSize"))
                if (!$util.isInteger(message.groupSize) && !(message.groupSize && $util.isInteger(message.groupSize.low) && $util.isInteger(message.groupSize.high)))
                    return "groupSize: integer|Long expected";
            return null;
        };

        /**
         * Creates a CardDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.CardDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.CardDef} CardDef
         */
        CardDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.CardDef)
                return object;
            let message = new $root.epoch_proto.CardDef();
            switch (object.type) {
            default:
                if (typeof object.type === "number") {
                    message.type = object.type;
                    break;
                }
                break;
            case "WidgetUnspecified":
            case 0:
                message.type = 0;
                break;
            case "WidgetCard":
            case 1:
                message.type = 1;
                break;
            case "WidgetLines":
            case 2:
                message.type = 2;
                break;
            case "WidgetBar":
            case 3:
                message.type = 3;
                break;
            case "WidgetDataTable":
            case 4:
                message.type = 4;
                break;
            case "WidgetXRange":
            case 5:
                message.type = 5;
                break;
            case "WidgetHistogram":
            case 6:
                message.type = 6;
                break;
            case "WidgetPie":
            case 7:
                message.type = 7;
                break;
            case "WidgetHeatMap":
            case 8:
                message.type = 8;
                break;
            case "WidgetBoxPlot":
            case 9:
                message.type = 9;
                break;
            case "WidgetArea":
            case 10:
                message.type = 10;
                break;
            case "WidgetColumn":
            case 11:
                message.type = 11;
                break;
            case "WidgetScatter":
            case 12:
                message.type = 12;
                break;
            case "WidgetWaterfall":
            case 13:
                message.type = 13;
                break;
            case "WidgetSpline":
            case 14:
                message.type = 14;
                break;
            case "WidgetBubble":
            case 15:
                message.type = 15;
                break;
            case "WidgetTreemap":
            case 16:
                message.type = 16;
                break;
            case "WidgetSankey":
            case 17:
                message.type = 17;
                break;
            case "WidgetAreaRange":
            case 18:
                message.type = 18;
                break;
            case "WidgetGauge":
            case 19:
                message.type = 19;
                break;
            case "WidgetBullet":
            case 20:
                message.type = 20;
                break;
            case "WidgetTimeline":
            case 21:
                message.type = 21;
                break;
            case "WidgetErrorBar":
            case 22:
                message.type = 22;
                break;
            case "WidgetBellCurve":
            case 23:
                message.type = 23;
                break;
            case "WidgetNumericErrorBar":
            case 24:
                message.type = 24;
                break;
            }
            if (object.category != null)
                message.category = String(object.category);
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.CardDef.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.CardDef.data: object expected");
                    message.data[i] = $root.epoch_proto.CardData.fromObject(object.data[i]);
                }
            }
            if (object.groupSize != null)
                if ($util.Long)
                    (message.groupSize = $util.Long.fromValue(object.groupSize)).unsigned = true;
                else if (typeof object.groupSize === "string")
                    message.groupSize = parseInt(object.groupSize, 10);
                else if (typeof object.groupSize === "number")
                    message.groupSize = object.groupSize;
                else if (typeof object.groupSize === "object")
                    message.groupSize = new $util.LongBits(object.groupSize.low >>> 0, object.groupSize.high >>> 0).toNumber(true);
            return message;
        };

        /**
         * Creates a plain object from a CardDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.CardDef
         * @static
         * @param {epoch_proto.CardDef} message CardDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CardDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.data = [];
            if (options.defaults) {
                object.type = options.enums === String ? "WidgetUnspecified" : 0;
                object.category = "";
                if ($util.Long) {
                    let long = new $util.Long(0, 0, true);
                    object.groupSize = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.groupSize = options.longs === String ? "0" : 0;
            }
            if (message.type != null && message.hasOwnProperty("type"))
                object.type = options.enums === String ? $root.epoch_proto.EpochFolioDashboardWidget[message.type] === undefined ? message.type : $root.epoch_proto.EpochFolioDashboardWidget[message.type] : message.type;
            if (message.category != null && message.hasOwnProperty("category"))
                object.category = message.category;
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.CardData.toObject(message.data[j], options);
            }
            if (message.groupSize != null && message.hasOwnProperty("groupSize"))
                if (typeof message.groupSize === "number")
                    object.groupSize = options.longs === String ? String(message.groupSize) : message.groupSize;
                else
                    object.groupSize = options.longs === String ? $util.Long.prototype.toString.call(message.groupSize) : options.longs === Number ? new $util.LongBits(message.groupSize.low >>> 0, message.groupSize.high >>> 0).toNumber(true) : message.groupSize;
            return object;
        };

        /**
         * Converts this CardDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.CardDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CardDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CardDef
         * @function getTypeUrl
         * @memberof epoch_proto.CardDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CardDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.CardDef";
        };

        return CardDef;
    })();

    epoch_proto.LinesDef = (function() {

        /**
         * Properties of a LinesDef.
         * @memberof epoch_proto
         * @interface ILinesDef
         * @property {epoch_proto.IChartDef|null} [chartDef] LinesDef chartDef
         * @property {Array.<epoch_proto.ILine>|null} [lines] LinesDef lines
         * @property {Array.<epoch_proto.IStraightLineDef>|null} [straightLines] LinesDef straightLines
         * @property {Array.<epoch_proto.IBand>|null} [yPlotBands] LinesDef yPlotBands
         * @property {Array.<epoch_proto.IBand>|null} [xPlotBands] LinesDef xPlotBands
         * @property {epoch_proto.ILine|null} [overlay] LinesDef overlay
         * @property {boolean|null} [stacked] LinesDef stacked
         */

        /**
         * Constructs a new LinesDef.
         * @memberof epoch_proto
         * @classdesc Represents a LinesDef.
         * @implements ILinesDef
         * @constructor
         * @param {epoch_proto.ILinesDef=} [properties] Properties to set
         */
        function LinesDef(properties) {
            this.lines = [];
            this.straightLines = [];
            this.yPlotBands = [];
            this.xPlotBands = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * LinesDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.LinesDef
         * @instance
         */
        LinesDef.prototype.chartDef = null;

        /**
         * LinesDef lines.
         * @member {Array.<epoch_proto.ILine>} lines
         * @memberof epoch_proto.LinesDef
         * @instance
         */
        LinesDef.prototype.lines = $util.emptyArray;

        /**
         * LinesDef straightLines.
         * @member {Array.<epoch_proto.IStraightLineDef>} straightLines
         * @memberof epoch_proto.LinesDef
         * @instance
         */
        LinesDef.prototype.straightLines = $util.emptyArray;

        /**
         * LinesDef yPlotBands.
         * @member {Array.<epoch_proto.IBand>} yPlotBands
         * @memberof epoch_proto.LinesDef
         * @instance
         */
        LinesDef.prototype.yPlotBands = $util.emptyArray;

        /**
         * LinesDef xPlotBands.
         * @member {Array.<epoch_proto.IBand>} xPlotBands
         * @memberof epoch_proto.LinesDef
         * @instance
         */
        LinesDef.prototype.xPlotBands = $util.emptyArray;

        /**
         * LinesDef overlay.
         * @member {epoch_proto.ILine|null|undefined} overlay
         * @memberof epoch_proto.LinesDef
         * @instance
         */
        LinesDef.prototype.overlay = null;

        /**
         * LinesDef stacked.
         * @member {boolean} stacked
         * @memberof epoch_proto.LinesDef
         * @instance
         */
        LinesDef.prototype.stacked = false;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(LinesDef.prototype, "_overlay", {
            get: $util.oneOfGetter($oneOfFields = ["overlay"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new LinesDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.LinesDef
         * @static
         * @param {epoch_proto.ILinesDef=} [properties] Properties to set
         * @returns {epoch_proto.LinesDef} LinesDef instance
         */
        LinesDef.create = function create(properties) {
            return new LinesDef(properties);
        };

        /**
         * Encodes the specified LinesDef message. Does not implicitly {@link epoch_proto.LinesDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.LinesDef
         * @static
         * @param {epoch_proto.ILinesDef} message LinesDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        LinesDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.lines != null && message.lines.length)
                for (let i = 0; i < message.lines.length; ++i)
                    $root.epoch_proto.Line.encode(message.lines[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.straightLines != null && message.straightLines.length)
                for (let i = 0; i < message.straightLines.length; ++i)
                    $root.epoch_proto.StraightLineDef.encode(message.straightLines[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.yPlotBands != null && message.yPlotBands.length)
                for (let i = 0; i < message.yPlotBands.length; ++i)
                    $root.epoch_proto.Band.encode(message.yPlotBands[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
            if (message.xPlotBands != null && message.xPlotBands.length)
                for (let i = 0; i < message.xPlotBands.length; ++i)
                    $root.epoch_proto.Band.encode(message.xPlotBands[i], writer.uint32(/* id 5, wireType 2 =*/42).fork()).ldelim();
            if (message.overlay != null && Object.hasOwnProperty.call(message, "overlay"))
                $root.epoch_proto.Line.encode(message.overlay, writer.uint32(/* id 6, wireType 2 =*/50).fork()).ldelim();
            if (message.stacked != null && Object.hasOwnProperty.call(message, "stacked"))
                writer.uint32(/* id 7, wireType 0 =*/56).bool(message.stacked);
            return writer;
        };

        /**
         * Encodes the specified LinesDef message, length delimited. Does not implicitly {@link epoch_proto.LinesDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.LinesDef
         * @static
         * @param {epoch_proto.ILinesDef} message LinesDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        LinesDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a LinesDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.LinesDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.LinesDef} LinesDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        LinesDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.LinesDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.lines && message.lines.length))
                            message.lines = [];
                        message.lines.push($root.epoch_proto.Line.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        if (!(message.straightLines && message.straightLines.length))
                            message.straightLines = [];
                        message.straightLines.push($root.epoch_proto.StraightLineDef.decode(reader, reader.uint32()));
                        break;
                    }
                case 4: {
                        if (!(message.yPlotBands && message.yPlotBands.length))
                            message.yPlotBands = [];
                        message.yPlotBands.push($root.epoch_proto.Band.decode(reader, reader.uint32()));
                        break;
                    }
                case 5: {
                        if (!(message.xPlotBands && message.xPlotBands.length))
                            message.xPlotBands = [];
                        message.xPlotBands.push($root.epoch_proto.Band.decode(reader, reader.uint32()));
                        break;
                    }
                case 6: {
                        message.overlay = $root.epoch_proto.Line.decode(reader, reader.uint32());
                        break;
                    }
                case 7: {
                        message.stacked = reader.bool();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a LinesDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.LinesDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.LinesDef} LinesDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        LinesDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a LinesDef message.
         * @function verify
         * @memberof epoch_proto.LinesDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        LinesDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.lines != null && message.hasOwnProperty("lines")) {
                if (!Array.isArray(message.lines))
                    return "lines: array expected";
                for (let i = 0; i < message.lines.length; ++i) {
                    let error = $root.epoch_proto.Line.verify(message.lines[i]);
                    if (error)
                        return "lines." + error;
                }
            }
            if (message.straightLines != null && message.hasOwnProperty("straightLines")) {
                if (!Array.isArray(message.straightLines))
                    return "straightLines: array expected";
                for (let i = 0; i < message.straightLines.length; ++i) {
                    let error = $root.epoch_proto.StraightLineDef.verify(message.straightLines[i]);
                    if (error)
                        return "straightLines." + error;
                }
            }
            if (message.yPlotBands != null && message.hasOwnProperty("yPlotBands")) {
                if (!Array.isArray(message.yPlotBands))
                    return "yPlotBands: array expected";
                for (let i = 0; i < message.yPlotBands.length; ++i) {
                    let error = $root.epoch_proto.Band.verify(message.yPlotBands[i]);
                    if (error)
                        return "yPlotBands." + error;
                }
            }
            if (message.xPlotBands != null && message.hasOwnProperty("xPlotBands")) {
                if (!Array.isArray(message.xPlotBands))
                    return "xPlotBands: array expected";
                for (let i = 0; i < message.xPlotBands.length; ++i) {
                    let error = $root.epoch_proto.Band.verify(message.xPlotBands[i]);
                    if (error)
                        return "xPlotBands." + error;
                }
            }
            if (message.overlay != null && message.hasOwnProperty("overlay")) {
                properties._overlay = 1;
                {
                    let error = $root.epoch_proto.Line.verify(message.overlay);
                    if (error)
                        return "overlay." + error;
                }
            }
            if (message.stacked != null && message.hasOwnProperty("stacked"))
                if (typeof message.stacked !== "boolean")
                    return "stacked: boolean expected";
            return null;
        };

        /**
         * Creates a LinesDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.LinesDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.LinesDef} LinesDef
         */
        LinesDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.LinesDef)
                return object;
            let message = new $root.epoch_proto.LinesDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.LinesDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.lines) {
                if (!Array.isArray(object.lines))
                    throw TypeError(".epoch_proto.LinesDef.lines: array expected");
                message.lines = [];
                for (let i = 0; i < object.lines.length; ++i) {
                    if (typeof object.lines[i] !== "object")
                        throw TypeError(".epoch_proto.LinesDef.lines: object expected");
                    message.lines[i] = $root.epoch_proto.Line.fromObject(object.lines[i]);
                }
            }
            if (object.straightLines) {
                if (!Array.isArray(object.straightLines))
                    throw TypeError(".epoch_proto.LinesDef.straightLines: array expected");
                message.straightLines = [];
                for (let i = 0; i < object.straightLines.length; ++i) {
                    if (typeof object.straightLines[i] !== "object")
                        throw TypeError(".epoch_proto.LinesDef.straightLines: object expected");
                    message.straightLines[i] = $root.epoch_proto.StraightLineDef.fromObject(object.straightLines[i]);
                }
            }
            if (object.yPlotBands) {
                if (!Array.isArray(object.yPlotBands))
                    throw TypeError(".epoch_proto.LinesDef.yPlotBands: array expected");
                message.yPlotBands = [];
                for (let i = 0; i < object.yPlotBands.length; ++i) {
                    if (typeof object.yPlotBands[i] !== "object")
                        throw TypeError(".epoch_proto.LinesDef.yPlotBands: object expected");
                    message.yPlotBands[i] = $root.epoch_proto.Band.fromObject(object.yPlotBands[i]);
                }
            }
            if (object.xPlotBands) {
                if (!Array.isArray(object.xPlotBands))
                    throw TypeError(".epoch_proto.LinesDef.xPlotBands: array expected");
                message.xPlotBands = [];
                for (let i = 0; i < object.xPlotBands.length; ++i) {
                    if (typeof object.xPlotBands[i] !== "object")
                        throw TypeError(".epoch_proto.LinesDef.xPlotBands: object expected");
                    message.xPlotBands[i] = $root.epoch_proto.Band.fromObject(object.xPlotBands[i]);
                }
            }
            if (object.overlay != null) {
                if (typeof object.overlay !== "object")
                    throw TypeError(".epoch_proto.LinesDef.overlay: object expected");
                message.overlay = $root.epoch_proto.Line.fromObject(object.overlay);
            }
            if (object.stacked != null)
                message.stacked = Boolean(object.stacked);
            return message;
        };

        /**
         * Creates a plain object from a LinesDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.LinesDef
         * @static
         * @param {epoch_proto.LinesDef} message LinesDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        LinesDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults) {
                object.lines = [];
                object.straightLines = [];
                object.yPlotBands = [];
                object.xPlotBands = [];
            }
            if (options.defaults) {
                object.chartDef = null;
                object.stacked = false;
            }
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.lines && message.lines.length) {
                object.lines = [];
                for (let j = 0; j < message.lines.length; ++j)
                    object.lines[j] = $root.epoch_proto.Line.toObject(message.lines[j], options);
            }
            if (message.straightLines && message.straightLines.length) {
                object.straightLines = [];
                for (let j = 0; j < message.straightLines.length; ++j)
                    object.straightLines[j] = $root.epoch_proto.StraightLineDef.toObject(message.straightLines[j], options);
            }
            if (message.yPlotBands && message.yPlotBands.length) {
                object.yPlotBands = [];
                for (let j = 0; j < message.yPlotBands.length; ++j)
                    object.yPlotBands[j] = $root.epoch_proto.Band.toObject(message.yPlotBands[j], options);
            }
            if (message.xPlotBands && message.xPlotBands.length) {
                object.xPlotBands = [];
                for (let j = 0; j < message.xPlotBands.length; ++j)
                    object.xPlotBands[j] = $root.epoch_proto.Band.toObject(message.xPlotBands[j], options);
            }
            if (message.overlay != null && message.hasOwnProperty("overlay")) {
                object.overlay = $root.epoch_proto.Line.toObject(message.overlay, options);
                if (options.oneofs)
                    object._overlay = "overlay";
            }
            if (message.stacked != null && message.hasOwnProperty("stacked"))
                object.stacked = message.stacked;
            return object;
        };

        /**
         * Converts this LinesDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.LinesDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        LinesDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for LinesDef
         * @function getTypeUrl
         * @memberof epoch_proto.LinesDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        LinesDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.LinesDef";
        };

        return LinesDef;
    })();

    epoch_proto.NumericLinesDef = (function() {

        /**
         * Properties of a NumericLinesDef.
         * @memberof epoch_proto
         * @interface INumericLinesDef
         * @property {epoch_proto.IChartDef|null} [chartDef] NumericLinesDef chartDef
         * @property {Array.<epoch_proto.INumericLine>|null} [lines] NumericLinesDef lines
         * @property {Array.<epoch_proto.IStraightLineDef>|null} [straightLines] NumericLinesDef straightLines
         * @property {Array.<epoch_proto.IBand>|null} [yPlotBands] NumericLinesDef yPlotBands
         * @property {Array.<epoch_proto.IBand>|null} [xPlotBands] NumericLinesDef xPlotBands
         * @property {epoch_proto.INumericLine|null} [overlay] NumericLinesDef overlay
         * @property {boolean|null} [stacked] NumericLinesDef stacked
         */

        /**
         * Constructs a new NumericLinesDef.
         * @memberof epoch_proto
         * @classdesc Represents a NumericLinesDef.
         * @implements INumericLinesDef
         * @constructor
         * @param {epoch_proto.INumericLinesDef=} [properties] Properties to set
         */
        function NumericLinesDef(properties) {
            this.lines = [];
            this.straightLines = [];
            this.yPlotBands = [];
            this.xPlotBands = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NumericLinesDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.NumericLinesDef
         * @instance
         */
        NumericLinesDef.prototype.chartDef = null;

        /**
         * NumericLinesDef lines.
         * @member {Array.<epoch_proto.INumericLine>} lines
         * @memberof epoch_proto.NumericLinesDef
         * @instance
         */
        NumericLinesDef.prototype.lines = $util.emptyArray;

        /**
         * NumericLinesDef straightLines.
         * @member {Array.<epoch_proto.IStraightLineDef>} straightLines
         * @memberof epoch_proto.NumericLinesDef
         * @instance
         */
        NumericLinesDef.prototype.straightLines = $util.emptyArray;

        /**
         * NumericLinesDef yPlotBands.
         * @member {Array.<epoch_proto.IBand>} yPlotBands
         * @memberof epoch_proto.NumericLinesDef
         * @instance
         */
        NumericLinesDef.prototype.yPlotBands = $util.emptyArray;

        /**
         * NumericLinesDef xPlotBands.
         * @member {Array.<epoch_proto.IBand>} xPlotBands
         * @memberof epoch_proto.NumericLinesDef
         * @instance
         */
        NumericLinesDef.prototype.xPlotBands = $util.emptyArray;

        /**
         * NumericLinesDef overlay.
         * @member {epoch_proto.INumericLine|null|undefined} overlay
         * @memberof epoch_proto.NumericLinesDef
         * @instance
         */
        NumericLinesDef.prototype.overlay = null;

        /**
         * NumericLinesDef stacked.
         * @member {boolean} stacked
         * @memberof epoch_proto.NumericLinesDef
         * @instance
         */
        NumericLinesDef.prototype.stacked = false;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(NumericLinesDef.prototype, "_overlay", {
            get: $util.oneOfGetter($oneOfFields = ["overlay"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new NumericLinesDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.NumericLinesDef
         * @static
         * @param {epoch_proto.INumericLinesDef=} [properties] Properties to set
         * @returns {epoch_proto.NumericLinesDef} NumericLinesDef instance
         */
        NumericLinesDef.create = function create(properties) {
            return new NumericLinesDef(properties);
        };

        /**
         * Encodes the specified NumericLinesDef message. Does not implicitly {@link epoch_proto.NumericLinesDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.NumericLinesDef
         * @static
         * @param {epoch_proto.INumericLinesDef} message NumericLinesDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericLinesDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.lines != null && message.lines.length)
                for (let i = 0; i < message.lines.length; ++i)
                    $root.epoch_proto.NumericLine.encode(message.lines[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.straightLines != null && message.straightLines.length)
                for (let i = 0; i < message.straightLines.length; ++i)
                    $root.epoch_proto.StraightLineDef.encode(message.straightLines[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.yPlotBands != null && message.yPlotBands.length)
                for (let i = 0; i < message.yPlotBands.length; ++i)
                    $root.epoch_proto.Band.encode(message.yPlotBands[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
            if (message.xPlotBands != null && message.xPlotBands.length)
                for (let i = 0; i < message.xPlotBands.length; ++i)
                    $root.epoch_proto.Band.encode(message.xPlotBands[i], writer.uint32(/* id 5, wireType 2 =*/42).fork()).ldelim();
            if (message.overlay != null && Object.hasOwnProperty.call(message, "overlay"))
                $root.epoch_proto.NumericLine.encode(message.overlay, writer.uint32(/* id 6, wireType 2 =*/50).fork()).ldelim();
            if (message.stacked != null && Object.hasOwnProperty.call(message, "stacked"))
                writer.uint32(/* id 7, wireType 0 =*/56).bool(message.stacked);
            return writer;
        };

        /**
         * Encodes the specified NumericLinesDef message, length delimited. Does not implicitly {@link epoch_proto.NumericLinesDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.NumericLinesDef
         * @static
         * @param {epoch_proto.INumericLinesDef} message NumericLinesDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericLinesDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NumericLinesDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.NumericLinesDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.NumericLinesDef} NumericLinesDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericLinesDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.NumericLinesDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.lines && message.lines.length))
                            message.lines = [];
                        message.lines.push($root.epoch_proto.NumericLine.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        if (!(message.straightLines && message.straightLines.length))
                            message.straightLines = [];
                        message.straightLines.push($root.epoch_proto.StraightLineDef.decode(reader, reader.uint32()));
                        break;
                    }
                case 4: {
                        if (!(message.yPlotBands && message.yPlotBands.length))
                            message.yPlotBands = [];
                        message.yPlotBands.push($root.epoch_proto.Band.decode(reader, reader.uint32()));
                        break;
                    }
                case 5: {
                        if (!(message.xPlotBands && message.xPlotBands.length))
                            message.xPlotBands = [];
                        message.xPlotBands.push($root.epoch_proto.Band.decode(reader, reader.uint32()));
                        break;
                    }
                case 6: {
                        message.overlay = $root.epoch_proto.NumericLine.decode(reader, reader.uint32());
                        break;
                    }
                case 7: {
                        message.stacked = reader.bool();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NumericLinesDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.NumericLinesDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.NumericLinesDef} NumericLinesDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericLinesDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NumericLinesDef message.
         * @function verify
         * @memberof epoch_proto.NumericLinesDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NumericLinesDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.lines != null && message.hasOwnProperty("lines")) {
                if (!Array.isArray(message.lines))
                    return "lines: array expected";
                for (let i = 0; i < message.lines.length; ++i) {
                    let error = $root.epoch_proto.NumericLine.verify(message.lines[i]);
                    if (error)
                        return "lines." + error;
                }
            }
            if (message.straightLines != null && message.hasOwnProperty("straightLines")) {
                if (!Array.isArray(message.straightLines))
                    return "straightLines: array expected";
                for (let i = 0; i < message.straightLines.length; ++i) {
                    let error = $root.epoch_proto.StraightLineDef.verify(message.straightLines[i]);
                    if (error)
                        return "straightLines." + error;
                }
            }
            if (message.yPlotBands != null && message.hasOwnProperty("yPlotBands")) {
                if (!Array.isArray(message.yPlotBands))
                    return "yPlotBands: array expected";
                for (let i = 0; i < message.yPlotBands.length; ++i) {
                    let error = $root.epoch_proto.Band.verify(message.yPlotBands[i]);
                    if (error)
                        return "yPlotBands." + error;
                }
            }
            if (message.xPlotBands != null && message.hasOwnProperty("xPlotBands")) {
                if (!Array.isArray(message.xPlotBands))
                    return "xPlotBands: array expected";
                for (let i = 0; i < message.xPlotBands.length; ++i) {
                    let error = $root.epoch_proto.Band.verify(message.xPlotBands[i]);
                    if (error)
                        return "xPlotBands." + error;
                }
            }
            if (message.overlay != null && message.hasOwnProperty("overlay")) {
                properties._overlay = 1;
                {
                    let error = $root.epoch_proto.NumericLine.verify(message.overlay);
                    if (error)
                        return "overlay." + error;
                }
            }
            if (message.stacked != null && message.hasOwnProperty("stacked"))
                if (typeof message.stacked !== "boolean")
                    return "stacked: boolean expected";
            return null;
        };

        /**
         * Creates a NumericLinesDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.NumericLinesDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.NumericLinesDef} NumericLinesDef
         */
        NumericLinesDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.NumericLinesDef)
                return object;
            let message = new $root.epoch_proto.NumericLinesDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.NumericLinesDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.lines) {
                if (!Array.isArray(object.lines))
                    throw TypeError(".epoch_proto.NumericLinesDef.lines: array expected");
                message.lines = [];
                for (let i = 0; i < object.lines.length; ++i) {
                    if (typeof object.lines[i] !== "object")
                        throw TypeError(".epoch_proto.NumericLinesDef.lines: object expected");
                    message.lines[i] = $root.epoch_proto.NumericLine.fromObject(object.lines[i]);
                }
            }
            if (object.straightLines) {
                if (!Array.isArray(object.straightLines))
                    throw TypeError(".epoch_proto.NumericLinesDef.straightLines: array expected");
                message.straightLines = [];
                for (let i = 0; i < object.straightLines.length; ++i) {
                    if (typeof object.straightLines[i] !== "object")
                        throw TypeError(".epoch_proto.NumericLinesDef.straightLines: object expected");
                    message.straightLines[i] = $root.epoch_proto.StraightLineDef.fromObject(object.straightLines[i]);
                }
            }
            if (object.yPlotBands) {
                if (!Array.isArray(object.yPlotBands))
                    throw TypeError(".epoch_proto.NumericLinesDef.yPlotBands: array expected");
                message.yPlotBands = [];
                for (let i = 0; i < object.yPlotBands.length; ++i) {
                    if (typeof object.yPlotBands[i] !== "object")
                        throw TypeError(".epoch_proto.NumericLinesDef.yPlotBands: object expected");
                    message.yPlotBands[i] = $root.epoch_proto.Band.fromObject(object.yPlotBands[i]);
                }
            }
            if (object.xPlotBands) {
                if (!Array.isArray(object.xPlotBands))
                    throw TypeError(".epoch_proto.NumericLinesDef.xPlotBands: array expected");
                message.xPlotBands = [];
                for (let i = 0; i < object.xPlotBands.length; ++i) {
                    if (typeof object.xPlotBands[i] !== "object")
                        throw TypeError(".epoch_proto.NumericLinesDef.xPlotBands: object expected");
                    message.xPlotBands[i] = $root.epoch_proto.Band.fromObject(object.xPlotBands[i]);
                }
            }
            if (object.overlay != null) {
                if (typeof object.overlay !== "object")
                    throw TypeError(".epoch_proto.NumericLinesDef.overlay: object expected");
                message.overlay = $root.epoch_proto.NumericLine.fromObject(object.overlay);
            }
            if (object.stacked != null)
                message.stacked = Boolean(object.stacked);
            return message;
        };

        /**
         * Creates a plain object from a NumericLinesDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.NumericLinesDef
         * @static
         * @param {epoch_proto.NumericLinesDef} message NumericLinesDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NumericLinesDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults) {
                object.lines = [];
                object.straightLines = [];
                object.yPlotBands = [];
                object.xPlotBands = [];
            }
            if (options.defaults) {
                object.chartDef = null;
                object.stacked = false;
            }
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.lines && message.lines.length) {
                object.lines = [];
                for (let j = 0; j < message.lines.length; ++j)
                    object.lines[j] = $root.epoch_proto.NumericLine.toObject(message.lines[j], options);
            }
            if (message.straightLines && message.straightLines.length) {
                object.straightLines = [];
                for (let j = 0; j < message.straightLines.length; ++j)
                    object.straightLines[j] = $root.epoch_proto.StraightLineDef.toObject(message.straightLines[j], options);
            }
            if (message.yPlotBands && message.yPlotBands.length) {
                object.yPlotBands = [];
                for (let j = 0; j < message.yPlotBands.length; ++j)
                    object.yPlotBands[j] = $root.epoch_proto.Band.toObject(message.yPlotBands[j], options);
            }
            if (message.xPlotBands && message.xPlotBands.length) {
                object.xPlotBands = [];
                for (let j = 0; j < message.xPlotBands.length; ++j)
                    object.xPlotBands[j] = $root.epoch_proto.Band.toObject(message.xPlotBands[j], options);
            }
            if (message.overlay != null && message.hasOwnProperty("overlay")) {
                object.overlay = $root.epoch_proto.NumericLine.toObject(message.overlay, options);
                if (options.oneofs)
                    object._overlay = "overlay";
            }
            if (message.stacked != null && message.hasOwnProperty("stacked"))
                object.stacked = message.stacked;
            return object;
        };

        /**
         * Converts this NumericLinesDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.NumericLinesDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NumericLinesDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NumericLinesDef
         * @function getTypeUrl
         * @memberof epoch_proto.NumericLinesDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NumericLinesDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.NumericLinesDef";
        };

        return NumericLinesDef;
    })();

    epoch_proto.AreaDef = (function() {

        /**
         * Properties of an AreaDef.
         * @memberof epoch_proto
         * @interface IAreaDef
         * @property {epoch_proto.IChartDef|null} [chartDef] AreaDef chartDef
         * @property {Array.<epoch_proto.ILine>|null} [areas] AreaDef areas
         * @property {boolean|null} [stacked] AreaDef stacked
         * @property {epoch_proto.StackType|null} [stackType] AreaDef stackType
         */

        /**
         * Constructs a new AreaDef.
         * @memberof epoch_proto
         * @classdesc Represents an AreaDef.
         * @implements IAreaDef
         * @constructor
         * @param {epoch_proto.IAreaDef=} [properties] Properties to set
         */
        function AreaDef(properties) {
            this.areas = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * AreaDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.AreaDef
         * @instance
         */
        AreaDef.prototype.chartDef = null;

        /**
         * AreaDef areas.
         * @member {Array.<epoch_proto.ILine>} areas
         * @memberof epoch_proto.AreaDef
         * @instance
         */
        AreaDef.prototype.areas = $util.emptyArray;

        /**
         * AreaDef stacked.
         * @member {boolean} stacked
         * @memberof epoch_proto.AreaDef
         * @instance
         */
        AreaDef.prototype.stacked = false;

        /**
         * AreaDef stackType.
         * @member {epoch_proto.StackType|null|undefined} stackType
         * @memberof epoch_proto.AreaDef
         * @instance
         */
        AreaDef.prototype.stackType = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(AreaDef.prototype, "_stackType", {
            get: $util.oneOfGetter($oneOfFields = ["stackType"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new AreaDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.AreaDef
         * @static
         * @param {epoch_proto.IAreaDef=} [properties] Properties to set
         * @returns {epoch_proto.AreaDef} AreaDef instance
         */
        AreaDef.create = function create(properties) {
            return new AreaDef(properties);
        };

        /**
         * Encodes the specified AreaDef message. Does not implicitly {@link epoch_proto.AreaDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.AreaDef
         * @static
         * @param {epoch_proto.IAreaDef} message AreaDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AreaDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.areas != null && message.areas.length)
                for (let i = 0; i < message.areas.length; ++i)
                    $root.epoch_proto.Line.encode(message.areas[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.stacked != null && Object.hasOwnProperty.call(message, "stacked"))
                writer.uint32(/* id 3, wireType 0 =*/24).bool(message.stacked);
            if (message.stackType != null && Object.hasOwnProperty.call(message, "stackType"))
                writer.uint32(/* id 4, wireType 0 =*/32).int32(message.stackType);
            return writer;
        };

        /**
         * Encodes the specified AreaDef message, length delimited. Does not implicitly {@link epoch_proto.AreaDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.AreaDef
         * @static
         * @param {epoch_proto.IAreaDef} message AreaDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AreaDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an AreaDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.AreaDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.AreaDef} AreaDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AreaDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.AreaDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.areas && message.areas.length))
                            message.areas = [];
                        message.areas.push($root.epoch_proto.Line.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.stacked = reader.bool();
                        break;
                    }
                case 4: {
                        message.stackType = reader.int32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an AreaDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.AreaDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.AreaDef} AreaDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AreaDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an AreaDef message.
         * @function verify
         * @memberof epoch_proto.AreaDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        AreaDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.areas != null && message.hasOwnProperty("areas")) {
                if (!Array.isArray(message.areas))
                    return "areas: array expected";
                for (let i = 0; i < message.areas.length; ++i) {
                    let error = $root.epoch_proto.Line.verify(message.areas[i]);
                    if (error)
                        return "areas." + error;
                }
            }
            if (message.stacked != null && message.hasOwnProperty("stacked"))
                if (typeof message.stacked !== "boolean")
                    return "stacked: boolean expected";
            if (message.stackType != null && message.hasOwnProperty("stackType")) {
                properties._stackType = 1;
                switch (message.stackType) {
                default:
                    return "stackType: enum value expected";
                case 0:
                case 1:
                case 2:
                    break;
                }
            }
            return null;
        };

        /**
         * Creates an AreaDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.AreaDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.AreaDef} AreaDef
         */
        AreaDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.AreaDef)
                return object;
            let message = new $root.epoch_proto.AreaDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.AreaDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.areas) {
                if (!Array.isArray(object.areas))
                    throw TypeError(".epoch_proto.AreaDef.areas: array expected");
                message.areas = [];
                for (let i = 0; i < object.areas.length; ++i) {
                    if (typeof object.areas[i] !== "object")
                        throw TypeError(".epoch_proto.AreaDef.areas: object expected");
                    message.areas[i] = $root.epoch_proto.Line.fromObject(object.areas[i]);
                }
            }
            if (object.stacked != null)
                message.stacked = Boolean(object.stacked);
            switch (object.stackType) {
            default:
                if (typeof object.stackType === "number") {
                    message.stackType = object.stackType;
                    break;
                }
                break;
            case "StackTypeUnspecified":
            case 0:
                message.stackType = 0;
                break;
            case "StackTypeNormal":
            case 1:
                message.stackType = 1;
                break;
            case "StackTypePercent":
            case 2:
                message.stackType = 2;
                break;
            }
            return message;
        };

        /**
         * Creates a plain object from an AreaDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.AreaDef
         * @static
         * @param {epoch_proto.AreaDef} message AreaDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        AreaDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.areas = [];
            if (options.defaults) {
                object.chartDef = null;
                object.stacked = false;
            }
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.areas && message.areas.length) {
                object.areas = [];
                for (let j = 0; j < message.areas.length; ++j)
                    object.areas[j] = $root.epoch_proto.Line.toObject(message.areas[j], options);
            }
            if (message.stacked != null && message.hasOwnProperty("stacked"))
                object.stacked = message.stacked;
            if (message.stackType != null && message.hasOwnProperty("stackType")) {
                object.stackType = options.enums === String ? $root.epoch_proto.StackType[message.stackType] === undefined ? message.stackType : $root.epoch_proto.StackType[message.stackType] : message.stackType;
                if (options.oneofs)
                    object._stackType = "stackType";
            }
            return object;
        };

        /**
         * Converts this AreaDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.AreaDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        AreaDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for AreaDef
         * @function getTypeUrl
         * @memberof epoch_proto.AreaDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        AreaDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.AreaDef";
        };

        return AreaDef;
    })();

    epoch_proto.BarData = (function() {

        /**
         * Properties of a BarData.
         * @memberof epoch_proto
         * @interface IBarData
         * @property {string|null} [name] BarData name
         * @property {Array.<number>|null} [values] BarData values
         * @property {string|null} [stack] BarData stack
         */

        /**
         * Constructs a new BarData.
         * @memberof epoch_proto
         * @classdesc Represents a BarData.
         * @implements IBarData
         * @constructor
         * @param {epoch_proto.IBarData=} [properties] Properties to set
         */
        function BarData(properties) {
            this.values = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BarData name.
         * @member {string} name
         * @memberof epoch_proto.BarData
         * @instance
         */
        BarData.prototype.name = "";

        /**
         * BarData values.
         * @member {Array.<number>} values
         * @memberof epoch_proto.BarData
         * @instance
         */
        BarData.prototype.values = $util.emptyArray;

        /**
         * BarData stack.
         * @member {string|null|undefined} stack
         * @memberof epoch_proto.BarData
         * @instance
         */
        BarData.prototype.stack = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BarData.prototype, "_stack", {
            get: $util.oneOfGetter($oneOfFields = ["stack"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new BarData instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BarData
         * @static
         * @param {epoch_proto.IBarData=} [properties] Properties to set
         * @returns {epoch_proto.BarData} BarData instance
         */
        BarData.create = function create(properties) {
            return new BarData(properties);
        };

        /**
         * Encodes the specified BarData message. Does not implicitly {@link epoch_proto.BarData.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BarData
         * @static
         * @param {epoch_proto.IBarData} message BarData message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BarData.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.name);
            if (message.values != null && message.values.length) {
                writer.uint32(/* id 2, wireType 2 =*/18).fork();
                for (let i = 0; i < message.values.length; ++i)
                    writer.double(message.values[i]);
                writer.ldelim();
            }
            if (message.stack != null && Object.hasOwnProperty.call(message, "stack"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.stack);
            return writer;
        };

        /**
         * Encodes the specified BarData message, length delimited. Does not implicitly {@link epoch_proto.BarData.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BarData
         * @static
         * @param {epoch_proto.IBarData} message BarData message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BarData.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BarData message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BarData
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BarData} BarData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BarData.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BarData();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.name = reader.string();
                        break;
                    }
                case 2: {
                        if (!(message.values && message.values.length))
                            message.values = [];
                        if ((tag & 7) === 2) {
                            let end2 = reader.uint32() + reader.pos;
                            while (reader.pos < end2)
                                message.values.push(reader.double());
                        } else
                            message.values.push(reader.double());
                        break;
                    }
                case 3: {
                        message.stack = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BarData message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BarData
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BarData} BarData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BarData.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BarData message.
         * @function verify
         * @memberof epoch_proto.BarData
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BarData.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.values != null && message.hasOwnProperty("values")) {
                if (!Array.isArray(message.values))
                    return "values: array expected";
                for (let i = 0; i < message.values.length; ++i)
                    if (typeof message.values[i] !== "number")
                        return "values: number[] expected";
            }
            if (message.stack != null && message.hasOwnProperty("stack")) {
                properties._stack = 1;
                if (!$util.isString(message.stack))
                    return "stack: string expected";
            }
            return null;
        };

        /**
         * Creates a BarData message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BarData
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BarData} BarData
         */
        BarData.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BarData)
                return object;
            let message = new $root.epoch_proto.BarData();
            if (object.name != null)
                message.name = String(object.name);
            if (object.values) {
                if (!Array.isArray(object.values))
                    throw TypeError(".epoch_proto.BarData.values: array expected");
                message.values = [];
                for (let i = 0; i < object.values.length; ++i)
                    message.values[i] = Number(object.values[i]);
            }
            if (object.stack != null)
                message.stack = String(object.stack);
            return message;
        };

        /**
         * Creates a plain object from a BarData message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BarData
         * @static
         * @param {epoch_proto.BarData} message BarData
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BarData.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.values = [];
            if (options.defaults)
                object.name = "";
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.values && message.values.length) {
                object.values = [];
                for (let j = 0; j < message.values.length; ++j)
                    object.values[j] = options.json && !isFinite(message.values[j]) ? String(message.values[j]) : message.values[j];
            }
            if (message.stack != null && message.hasOwnProperty("stack")) {
                object.stack = message.stack;
                if (options.oneofs)
                    object._stack = "stack";
            }
            return object;
        };

        /**
         * Converts this BarData to JSON.
         * @function toJSON
         * @memberof epoch_proto.BarData
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BarData.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BarData
         * @function getTypeUrl
         * @memberof epoch_proto.BarData
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BarData.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BarData";
        };

        return BarData;
    })();

    epoch_proto.BarDef = (function() {

        /**
         * Properties of a BarDef.
         * @memberof epoch_proto
         * @interface IBarDef
         * @property {epoch_proto.IChartDef|null} [chartDef] BarDef chartDef
         * @property {Array.<epoch_proto.IBarData>|null} [data] BarDef data
         * @property {Array.<epoch_proto.IStraightLineDef>|null} [straightLines] BarDef straightLines
         * @property {number|null} [barWidth] BarDef barWidth
         * @property {boolean|null} [vertical] BarDef vertical
         * @property {boolean|null} [stacked] BarDef stacked
         * @property {epoch_proto.StackType|null} [stackType] BarDef stackType
         */

        /**
         * Constructs a new BarDef.
         * @memberof epoch_proto
         * @classdesc Represents a BarDef.
         * @implements IBarDef
         * @constructor
         * @param {epoch_proto.IBarDef=} [properties] Properties to set
         */
        function BarDef(properties) {
            this.data = [];
            this.straightLines = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BarDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.BarDef
         * @instance
         */
        BarDef.prototype.chartDef = null;

        /**
         * BarDef data.
         * @member {Array.<epoch_proto.IBarData>} data
         * @memberof epoch_proto.BarDef
         * @instance
         */
        BarDef.prototype.data = $util.emptyArray;

        /**
         * BarDef straightLines.
         * @member {Array.<epoch_proto.IStraightLineDef>} straightLines
         * @memberof epoch_proto.BarDef
         * @instance
         */
        BarDef.prototype.straightLines = $util.emptyArray;

        /**
         * BarDef barWidth.
         * @member {number|null|undefined} barWidth
         * @memberof epoch_proto.BarDef
         * @instance
         */
        BarDef.prototype.barWidth = null;

        /**
         * BarDef vertical.
         * @member {boolean} vertical
         * @memberof epoch_proto.BarDef
         * @instance
         */
        BarDef.prototype.vertical = false;

        /**
         * BarDef stacked.
         * @member {boolean} stacked
         * @memberof epoch_proto.BarDef
         * @instance
         */
        BarDef.prototype.stacked = false;

        /**
         * BarDef stackType.
         * @member {epoch_proto.StackType|null|undefined} stackType
         * @memberof epoch_proto.BarDef
         * @instance
         */
        BarDef.prototype.stackType = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BarDef.prototype, "_barWidth", {
            get: $util.oneOfGetter($oneOfFields = ["barWidth"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BarDef.prototype, "_stackType", {
            get: $util.oneOfGetter($oneOfFields = ["stackType"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new BarDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BarDef
         * @static
         * @param {epoch_proto.IBarDef=} [properties] Properties to set
         * @returns {epoch_proto.BarDef} BarDef instance
         */
        BarDef.create = function create(properties) {
            return new BarDef(properties);
        };

        /**
         * Encodes the specified BarDef message. Does not implicitly {@link epoch_proto.BarDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BarDef
         * @static
         * @param {epoch_proto.IBarDef} message BarDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BarDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.BarData.encode(message.data[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.straightLines != null && message.straightLines.length)
                for (let i = 0; i < message.straightLines.length; ++i)
                    $root.epoch_proto.StraightLineDef.encode(message.straightLines[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.barWidth != null && Object.hasOwnProperty.call(message, "barWidth"))
                writer.uint32(/* id 4, wireType 0 =*/32).uint32(message.barWidth);
            if (message.vertical != null && Object.hasOwnProperty.call(message, "vertical"))
                writer.uint32(/* id 5, wireType 0 =*/40).bool(message.vertical);
            if (message.stacked != null && Object.hasOwnProperty.call(message, "stacked"))
                writer.uint32(/* id 6, wireType 0 =*/48).bool(message.stacked);
            if (message.stackType != null && Object.hasOwnProperty.call(message, "stackType"))
                writer.uint32(/* id 7, wireType 0 =*/56).int32(message.stackType);
            return writer;
        };

        /**
         * Encodes the specified BarDef message, length delimited. Does not implicitly {@link epoch_proto.BarDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BarDef
         * @static
         * @param {epoch_proto.IBarDef} message BarDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BarDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BarDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BarDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BarDef} BarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BarDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BarDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.BarData.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        if (!(message.straightLines && message.straightLines.length))
                            message.straightLines = [];
                        message.straightLines.push($root.epoch_proto.StraightLineDef.decode(reader, reader.uint32()));
                        break;
                    }
                case 4: {
                        message.barWidth = reader.uint32();
                        break;
                    }
                case 5: {
                        message.vertical = reader.bool();
                        break;
                    }
                case 6: {
                        message.stacked = reader.bool();
                        break;
                    }
                case 7: {
                        message.stackType = reader.int32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BarDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BarDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BarDef} BarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BarDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BarDef message.
         * @function verify
         * @memberof epoch_proto.BarDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BarDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.BarData.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            if (message.straightLines != null && message.hasOwnProperty("straightLines")) {
                if (!Array.isArray(message.straightLines))
                    return "straightLines: array expected";
                for (let i = 0; i < message.straightLines.length; ++i) {
                    let error = $root.epoch_proto.StraightLineDef.verify(message.straightLines[i]);
                    if (error)
                        return "straightLines." + error;
                }
            }
            if (message.barWidth != null && message.hasOwnProperty("barWidth")) {
                properties._barWidth = 1;
                if (!$util.isInteger(message.barWidth))
                    return "barWidth: integer expected";
            }
            if (message.vertical != null && message.hasOwnProperty("vertical"))
                if (typeof message.vertical !== "boolean")
                    return "vertical: boolean expected";
            if (message.stacked != null && message.hasOwnProperty("stacked"))
                if (typeof message.stacked !== "boolean")
                    return "stacked: boolean expected";
            if (message.stackType != null && message.hasOwnProperty("stackType")) {
                properties._stackType = 1;
                switch (message.stackType) {
                default:
                    return "stackType: enum value expected";
                case 0:
                case 1:
                case 2:
                    break;
                }
            }
            return null;
        };

        /**
         * Creates a BarDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BarDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BarDef} BarDef
         */
        BarDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BarDef)
                return object;
            let message = new $root.epoch_proto.BarDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.BarDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.BarDef.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.BarDef.data: object expected");
                    message.data[i] = $root.epoch_proto.BarData.fromObject(object.data[i]);
                }
            }
            if (object.straightLines) {
                if (!Array.isArray(object.straightLines))
                    throw TypeError(".epoch_proto.BarDef.straightLines: array expected");
                message.straightLines = [];
                for (let i = 0; i < object.straightLines.length; ++i) {
                    if (typeof object.straightLines[i] !== "object")
                        throw TypeError(".epoch_proto.BarDef.straightLines: object expected");
                    message.straightLines[i] = $root.epoch_proto.StraightLineDef.fromObject(object.straightLines[i]);
                }
            }
            if (object.barWidth != null)
                message.barWidth = object.barWidth >>> 0;
            if (object.vertical != null)
                message.vertical = Boolean(object.vertical);
            if (object.stacked != null)
                message.stacked = Boolean(object.stacked);
            switch (object.stackType) {
            default:
                if (typeof object.stackType === "number") {
                    message.stackType = object.stackType;
                    break;
                }
                break;
            case "StackTypeUnspecified":
            case 0:
                message.stackType = 0;
                break;
            case "StackTypeNormal":
            case 1:
                message.stackType = 1;
                break;
            case "StackTypePercent":
            case 2:
                message.stackType = 2;
                break;
            }
            return message;
        };

        /**
         * Creates a plain object from a BarDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BarDef
         * @static
         * @param {epoch_proto.BarDef} message BarDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BarDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults) {
                object.data = [];
                object.straightLines = [];
            }
            if (options.defaults) {
                object.chartDef = null;
                object.vertical = false;
                object.stacked = false;
            }
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.BarData.toObject(message.data[j], options);
            }
            if (message.straightLines && message.straightLines.length) {
                object.straightLines = [];
                for (let j = 0; j < message.straightLines.length; ++j)
                    object.straightLines[j] = $root.epoch_proto.StraightLineDef.toObject(message.straightLines[j], options);
            }
            if (message.barWidth != null && message.hasOwnProperty("barWidth")) {
                object.barWidth = message.barWidth;
                if (options.oneofs)
                    object._barWidth = "barWidth";
            }
            if (message.vertical != null && message.hasOwnProperty("vertical"))
                object.vertical = message.vertical;
            if (message.stacked != null && message.hasOwnProperty("stacked"))
                object.stacked = message.stacked;
            if (message.stackType != null && message.hasOwnProperty("stackType")) {
                object.stackType = options.enums === String ? $root.epoch_proto.StackType[message.stackType] === undefined ? message.stackType : $root.epoch_proto.StackType[message.stackType] : message.stackType;
                if (options.oneofs)
                    object._stackType = "stackType";
            }
            return object;
        };

        /**
         * Converts this BarDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.BarDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BarDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BarDef
         * @function getTypeUrl
         * @memberof epoch_proto.BarDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BarDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BarDef";
        };

        return BarDef;
    })();

    epoch_proto.HeatMapPoint = (function() {

        /**
         * Properties of a HeatMapPoint.
         * @memberof epoch_proto
         * @interface IHeatMapPoint
         * @property {number|Long|null} [x] HeatMapPoint x
         * @property {number|Long|null} [y] HeatMapPoint y
         * @property {number|null} [value] HeatMapPoint value
         */

        /**
         * Constructs a new HeatMapPoint.
         * @memberof epoch_proto
         * @classdesc Represents a HeatMapPoint.
         * @implements IHeatMapPoint
         * @constructor
         * @param {epoch_proto.IHeatMapPoint=} [properties] Properties to set
         */
        function HeatMapPoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * HeatMapPoint x.
         * @member {number|Long} x
         * @memberof epoch_proto.HeatMapPoint
         * @instance
         */
        HeatMapPoint.prototype.x = $util.Long ? $util.Long.fromBits(0,0,true) : 0;

        /**
         * HeatMapPoint y.
         * @member {number|Long} y
         * @memberof epoch_proto.HeatMapPoint
         * @instance
         */
        HeatMapPoint.prototype.y = $util.Long ? $util.Long.fromBits(0,0,true) : 0;

        /**
         * HeatMapPoint value.
         * @member {number} value
         * @memberof epoch_proto.HeatMapPoint
         * @instance
         */
        HeatMapPoint.prototype.value = 0;

        /**
         * Creates a new HeatMapPoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.HeatMapPoint
         * @static
         * @param {epoch_proto.IHeatMapPoint=} [properties] Properties to set
         * @returns {epoch_proto.HeatMapPoint} HeatMapPoint instance
         */
        HeatMapPoint.create = function create(properties) {
            return new HeatMapPoint(properties);
        };

        /**
         * Encodes the specified HeatMapPoint message. Does not implicitly {@link epoch_proto.HeatMapPoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.HeatMapPoint
         * @static
         * @param {epoch_proto.IHeatMapPoint} message HeatMapPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        HeatMapPoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 0 =*/8).uint64(message.x);
            if (message.y != null && Object.hasOwnProperty.call(message, "y"))
                writer.uint32(/* id 2, wireType 0 =*/16).uint64(message.y);
            if (message.value != null && Object.hasOwnProperty.call(message, "value"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.value);
            return writer;
        };

        /**
         * Encodes the specified HeatMapPoint message, length delimited. Does not implicitly {@link epoch_proto.HeatMapPoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.HeatMapPoint
         * @static
         * @param {epoch_proto.IHeatMapPoint} message HeatMapPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        HeatMapPoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a HeatMapPoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.HeatMapPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.HeatMapPoint} HeatMapPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        HeatMapPoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.HeatMapPoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.uint64();
                        break;
                    }
                case 2: {
                        message.y = reader.uint64();
                        break;
                    }
                case 3: {
                        message.value = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a HeatMapPoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.HeatMapPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.HeatMapPoint} HeatMapPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        HeatMapPoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a HeatMapPoint message.
         * @function verify
         * @memberof epoch_proto.HeatMapPoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        HeatMapPoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.x != null && message.hasOwnProperty("x"))
                if (!$util.isInteger(message.x) && !(message.x && $util.isInteger(message.x.low) && $util.isInteger(message.x.high)))
                    return "x: integer|Long expected";
            if (message.y != null && message.hasOwnProperty("y"))
                if (!$util.isInteger(message.y) && !(message.y && $util.isInteger(message.y.low) && $util.isInteger(message.y.high)))
                    return "y: integer|Long expected";
            if (message.value != null && message.hasOwnProperty("value"))
                if (typeof message.value !== "number")
                    return "value: number expected";
            return null;
        };

        /**
         * Creates a HeatMapPoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.HeatMapPoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.HeatMapPoint} HeatMapPoint
         */
        HeatMapPoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.HeatMapPoint)
                return object;
            let message = new $root.epoch_proto.HeatMapPoint();
            if (object.x != null)
                if ($util.Long)
                    (message.x = $util.Long.fromValue(object.x)).unsigned = true;
                else if (typeof object.x === "string")
                    message.x = parseInt(object.x, 10);
                else if (typeof object.x === "number")
                    message.x = object.x;
                else if (typeof object.x === "object")
                    message.x = new $util.LongBits(object.x.low >>> 0, object.x.high >>> 0).toNumber(true);
            if (object.y != null)
                if ($util.Long)
                    (message.y = $util.Long.fromValue(object.y)).unsigned = true;
                else if (typeof object.y === "string")
                    message.y = parseInt(object.y, 10);
                else if (typeof object.y === "number")
                    message.y = object.y;
                else if (typeof object.y === "object")
                    message.y = new $util.LongBits(object.y.low >>> 0, object.y.high >>> 0).toNumber(true);
            if (object.value != null)
                message.value = Number(object.value);
            return message;
        };

        /**
         * Creates a plain object from a HeatMapPoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.HeatMapPoint
         * @static
         * @param {epoch_proto.HeatMapPoint} message HeatMapPoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        HeatMapPoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                if ($util.Long) {
                    let long = new $util.Long(0, 0, true);
                    object.x = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.x = options.longs === String ? "0" : 0;
                if ($util.Long) {
                    let long = new $util.Long(0, 0, true);
                    object.y = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.y = options.longs === String ? "0" : 0;
                object.value = 0;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x === "number")
                    object.x = options.longs === String ? String(message.x) : message.x;
                else
                    object.x = options.longs === String ? $util.Long.prototype.toString.call(message.x) : options.longs === Number ? new $util.LongBits(message.x.low >>> 0, message.x.high >>> 0).toNumber(true) : message.x;
            if (message.y != null && message.hasOwnProperty("y"))
                if (typeof message.y === "number")
                    object.y = options.longs === String ? String(message.y) : message.y;
                else
                    object.y = options.longs === String ? $util.Long.prototype.toString.call(message.y) : options.longs === Number ? new $util.LongBits(message.y.low >>> 0, message.y.high >>> 0).toNumber(true) : message.y;
            if (message.value != null && message.hasOwnProperty("value"))
                object.value = options.json && !isFinite(message.value) ? String(message.value) : message.value;
            return object;
        };

        /**
         * Converts this HeatMapPoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.HeatMapPoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        HeatMapPoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for HeatMapPoint
         * @function getTypeUrl
         * @memberof epoch_proto.HeatMapPoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        HeatMapPoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.HeatMapPoint";
        };

        return HeatMapPoint;
    })();

    epoch_proto.HeatMapDef = (function() {

        /**
         * Properties of a HeatMapDef.
         * @memberof epoch_proto
         * @interface IHeatMapDef
         * @property {epoch_proto.IChartDef|null} [chartDef] HeatMapDef chartDef
         * @property {Array.<epoch_proto.IHeatMapPoint>|null} [points] HeatMapDef points
         */

        /**
         * Constructs a new HeatMapDef.
         * @memberof epoch_proto
         * @classdesc Represents a HeatMapDef.
         * @implements IHeatMapDef
         * @constructor
         * @param {epoch_proto.IHeatMapDef=} [properties] Properties to set
         */
        function HeatMapDef(properties) {
            this.points = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * HeatMapDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.HeatMapDef
         * @instance
         */
        HeatMapDef.prototype.chartDef = null;

        /**
         * HeatMapDef points.
         * @member {Array.<epoch_proto.IHeatMapPoint>} points
         * @memberof epoch_proto.HeatMapDef
         * @instance
         */
        HeatMapDef.prototype.points = $util.emptyArray;

        /**
         * Creates a new HeatMapDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.HeatMapDef
         * @static
         * @param {epoch_proto.IHeatMapDef=} [properties] Properties to set
         * @returns {epoch_proto.HeatMapDef} HeatMapDef instance
         */
        HeatMapDef.create = function create(properties) {
            return new HeatMapDef(properties);
        };

        /**
         * Encodes the specified HeatMapDef message. Does not implicitly {@link epoch_proto.HeatMapDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.HeatMapDef
         * @static
         * @param {epoch_proto.IHeatMapDef} message HeatMapDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        HeatMapDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.points != null && message.points.length)
                for (let i = 0; i < message.points.length; ++i)
                    $root.epoch_proto.HeatMapPoint.encode(message.points[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified HeatMapDef message, length delimited. Does not implicitly {@link epoch_proto.HeatMapDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.HeatMapDef
         * @static
         * @param {epoch_proto.IHeatMapDef} message HeatMapDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        HeatMapDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a HeatMapDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.HeatMapDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.HeatMapDef} HeatMapDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        HeatMapDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.HeatMapDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.points && message.points.length))
                            message.points = [];
                        message.points.push($root.epoch_proto.HeatMapPoint.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a HeatMapDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.HeatMapDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.HeatMapDef} HeatMapDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        HeatMapDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a HeatMapDef message.
         * @function verify
         * @memberof epoch_proto.HeatMapDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        HeatMapDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.points != null && message.hasOwnProperty("points")) {
                if (!Array.isArray(message.points))
                    return "points: array expected";
                for (let i = 0; i < message.points.length; ++i) {
                    let error = $root.epoch_proto.HeatMapPoint.verify(message.points[i]);
                    if (error)
                        return "points." + error;
                }
            }
            return null;
        };

        /**
         * Creates a HeatMapDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.HeatMapDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.HeatMapDef} HeatMapDef
         */
        HeatMapDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.HeatMapDef)
                return object;
            let message = new $root.epoch_proto.HeatMapDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.HeatMapDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.points) {
                if (!Array.isArray(object.points))
                    throw TypeError(".epoch_proto.HeatMapDef.points: array expected");
                message.points = [];
                for (let i = 0; i < object.points.length; ++i) {
                    if (typeof object.points[i] !== "object")
                        throw TypeError(".epoch_proto.HeatMapDef.points: object expected");
                    message.points[i] = $root.epoch_proto.HeatMapPoint.fromObject(object.points[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a HeatMapDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.HeatMapDef
         * @static
         * @param {epoch_proto.HeatMapDef} message HeatMapDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        HeatMapDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.points = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.points && message.points.length) {
                object.points = [];
                for (let j = 0; j < message.points.length; ++j)
                    object.points[j] = $root.epoch_proto.HeatMapPoint.toObject(message.points[j], options);
            }
            return object;
        };

        /**
         * Converts this HeatMapDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.HeatMapDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        HeatMapDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for HeatMapDef
         * @function getTypeUrl
         * @memberof epoch_proto.HeatMapDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        HeatMapDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.HeatMapDef";
        };

        return HeatMapDef;
    })();

    epoch_proto.HistogramDef = (function() {

        /**
         * Properties of a HistogramDef.
         * @memberof epoch_proto
         * @interface IHistogramDef
         * @property {epoch_proto.IChartDef|null} [chartDef] HistogramDef chartDef
         * @property {epoch_proto.IArray|null} [data] HistogramDef data
         * @property {Array.<epoch_proto.IStraightLineDef>|null} [straightLines] HistogramDef straightLines
         * @property {number|null} [binsCount] HistogramDef binsCount
         */

        /**
         * Constructs a new HistogramDef.
         * @memberof epoch_proto
         * @classdesc Represents a HistogramDef.
         * @implements IHistogramDef
         * @constructor
         * @param {epoch_proto.IHistogramDef=} [properties] Properties to set
         */
        function HistogramDef(properties) {
            this.straightLines = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * HistogramDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.HistogramDef
         * @instance
         */
        HistogramDef.prototype.chartDef = null;

        /**
         * HistogramDef data.
         * @member {epoch_proto.IArray|null|undefined} data
         * @memberof epoch_proto.HistogramDef
         * @instance
         */
        HistogramDef.prototype.data = null;

        /**
         * HistogramDef straightLines.
         * @member {Array.<epoch_proto.IStraightLineDef>} straightLines
         * @memberof epoch_proto.HistogramDef
         * @instance
         */
        HistogramDef.prototype.straightLines = $util.emptyArray;

        /**
         * HistogramDef binsCount.
         * @member {number|null|undefined} binsCount
         * @memberof epoch_proto.HistogramDef
         * @instance
         */
        HistogramDef.prototype.binsCount = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(HistogramDef.prototype, "_binsCount", {
            get: $util.oneOfGetter($oneOfFields = ["binsCount"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new HistogramDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.HistogramDef
         * @static
         * @param {epoch_proto.IHistogramDef=} [properties] Properties to set
         * @returns {epoch_proto.HistogramDef} HistogramDef instance
         */
        HistogramDef.create = function create(properties) {
            return new HistogramDef(properties);
        };

        /**
         * Encodes the specified HistogramDef message. Does not implicitly {@link epoch_proto.HistogramDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.HistogramDef
         * @static
         * @param {epoch_proto.IHistogramDef} message HistogramDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        HistogramDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.data != null && Object.hasOwnProperty.call(message, "data"))
                $root.epoch_proto.Array.encode(message.data, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.straightLines != null && message.straightLines.length)
                for (let i = 0; i < message.straightLines.length; ++i)
                    $root.epoch_proto.StraightLineDef.encode(message.straightLines[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.binsCount != null && Object.hasOwnProperty.call(message, "binsCount"))
                writer.uint32(/* id 4, wireType 0 =*/32).uint32(message.binsCount);
            return writer;
        };

        /**
         * Encodes the specified HistogramDef message, length delimited. Does not implicitly {@link epoch_proto.HistogramDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.HistogramDef
         * @static
         * @param {epoch_proto.IHistogramDef} message HistogramDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        HistogramDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a HistogramDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.HistogramDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.HistogramDef} HistogramDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        HistogramDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.HistogramDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        message.data = $root.epoch_proto.Array.decode(reader, reader.uint32());
                        break;
                    }
                case 3: {
                        if (!(message.straightLines && message.straightLines.length))
                            message.straightLines = [];
                        message.straightLines.push($root.epoch_proto.StraightLineDef.decode(reader, reader.uint32()));
                        break;
                    }
                case 4: {
                        message.binsCount = reader.uint32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a HistogramDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.HistogramDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.HistogramDef} HistogramDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        HistogramDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a HistogramDef message.
         * @function verify
         * @memberof epoch_proto.HistogramDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        HistogramDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.data != null && message.hasOwnProperty("data")) {
                let error = $root.epoch_proto.Array.verify(message.data);
                if (error)
                    return "data." + error;
            }
            if (message.straightLines != null && message.hasOwnProperty("straightLines")) {
                if (!Array.isArray(message.straightLines))
                    return "straightLines: array expected";
                for (let i = 0; i < message.straightLines.length; ++i) {
                    let error = $root.epoch_proto.StraightLineDef.verify(message.straightLines[i]);
                    if (error)
                        return "straightLines." + error;
                }
            }
            if (message.binsCount != null && message.hasOwnProperty("binsCount")) {
                properties._binsCount = 1;
                if (!$util.isInteger(message.binsCount))
                    return "binsCount: integer expected";
            }
            return null;
        };

        /**
         * Creates a HistogramDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.HistogramDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.HistogramDef} HistogramDef
         */
        HistogramDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.HistogramDef)
                return object;
            let message = new $root.epoch_proto.HistogramDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.HistogramDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.data != null) {
                if (typeof object.data !== "object")
                    throw TypeError(".epoch_proto.HistogramDef.data: object expected");
                message.data = $root.epoch_proto.Array.fromObject(object.data);
            }
            if (object.straightLines) {
                if (!Array.isArray(object.straightLines))
                    throw TypeError(".epoch_proto.HistogramDef.straightLines: array expected");
                message.straightLines = [];
                for (let i = 0; i < object.straightLines.length; ++i) {
                    if (typeof object.straightLines[i] !== "object")
                        throw TypeError(".epoch_proto.HistogramDef.straightLines: object expected");
                    message.straightLines[i] = $root.epoch_proto.StraightLineDef.fromObject(object.straightLines[i]);
                }
            }
            if (object.binsCount != null)
                message.binsCount = object.binsCount >>> 0;
            return message;
        };

        /**
         * Creates a plain object from a HistogramDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.HistogramDef
         * @static
         * @param {epoch_proto.HistogramDef} message HistogramDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        HistogramDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.straightLines = [];
            if (options.defaults) {
                object.chartDef = null;
                object.data = null;
            }
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.data != null && message.hasOwnProperty("data"))
                object.data = $root.epoch_proto.Array.toObject(message.data, options);
            if (message.straightLines && message.straightLines.length) {
                object.straightLines = [];
                for (let j = 0; j < message.straightLines.length; ++j)
                    object.straightLines[j] = $root.epoch_proto.StraightLineDef.toObject(message.straightLines[j], options);
            }
            if (message.binsCount != null && message.hasOwnProperty("binsCount")) {
                object.binsCount = message.binsCount;
                if (options.oneofs)
                    object._binsCount = "binsCount";
            }
            return object;
        };

        /**
         * Converts this HistogramDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.HistogramDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        HistogramDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for HistogramDef
         * @function getTypeUrl
         * @memberof epoch_proto.HistogramDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        HistogramDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.HistogramDef";
        };

        return HistogramDef;
    })();

    epoch_proto.BoxPlotDataPoint = (function() {

        /**
         * Properties of a BoxPlotDataPoint.
         * @memberof epoch_proto
         * @interface IBoxPlotDataPoint
         * @property {number|null} [low] BoxPlotDataPoint low
         * @property {number|null} [q1] BoxPlotDataPoint q1
         * @property {number|null} [median] BoxPlotDataPoint median
         * @property {number|null} [q3] BoxPlotDataPoint q3
         * @property {number|null} [high] BoxPlotDataPoint high
         */

        /**
         * Constructs a new BoxPlotDataPoint.
         * @memberof epoch_proto
         * @classdesc Represents a BoxPlotDataPoint.
         * @implements IBoxPlotDataPoint
         * @constructor
         * @param {epoch_proto.IBoxPlotDataPoint=} [properties] Properties to set
         */
        function BoxPlotDataPoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BoxPlotDataPoint low.
         * @member {number} low
         * @memberof epoch_proto.BoxPlotDataPoint
         * @instance
         */
        BoxPlotDataPoint.prototype.low = 0;

        /**
         * BoxPlotDataPoint q1.
         * @member {number} q1
         * @memberof epoch_proto.BoxPlotDataPoint
         * @instance
         */
        BoxPlotDataPoint.prototype.q1 = 0;

        /**
         * BoxPlotDataPoint median.
         * @member {number} median
         * @memberof epoch_proto.BoxPlotDataPoint
         * @instance
         */
        BoxPlotDataPoint.prototype.median = 0;

        /**
         * BoxPlotDataPoint q3.
         * @member {number} q3
         * @memberof epoch_proto.BoxPlotDataPoint
         * @instance
         */
        BoxPlotDataPoint.prototype.q3 = 0;

        /**
         * BoxPlotDataPoint high.
         * @member {number} high
         * @memberof epoch_proto.BoxPlotDataPoint
         * @instance
         */
        BoxPlotDataPoint.prototype.high = 0;

        /**
         * Creates a new BoxPlotDataPoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BoxPlotDataPoint
         * @static
         * @param {epoch_proto.IBoxPlotDataPoint=} [properties] Properties to set
         * @returns {epoch_proto.BoxPlotDataPoint} BoxPlotDataPoint instance
         */
        BoxPlotDataPoint.create = function create(properties) {
            return new BoxPlotDataPoint(properties);
        };

        /**
         * Encodes the specified BoxPlotDataPoint message. Does not implicitly {@link epoch_proto.BoxPlotDataPoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BoxPlotDataPoint
         * @static
         * @param {epoch_proto.IBoxPlotDataPoint} message BoxPlotDataPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BoxPlotDataPoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.low != null && Object.hasOwnProperty.call(message, "low"))
                writer.uint32(/* id 1, wireType 1 =*/9).double(message.low);
            if (message.q1 != null && Object.hasOwnProperty.call(message, "q1"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.q1);
            if (message.median != null && Object.hasOwnProperty.call(message, "median"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.median);
            if (message.q3 != null && Object.hasOwnProperty.call(message, "q3"))
                writer.uint32(/* id 4, wireType 1 =*/33).double(message.q3);
            if (message.high != null && Object.hasOwnProperty.call(message, "high"))
                writer.uint32(/* id 5, wireType 1 =*/41).double(message.high);
            return writer;
        };

        /**
         * Encodes the specified BoxPlotDataPoint message, length delimited. Does not implicitly {@link epoch_proto.BoxPlotDataPoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BoxPlotDataPoint
         * @static
         * @param {epoch_proto.IBoxPlotDataPoint} message BoxPlotDataPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BoxPlotDataPoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BoxPlotDataPoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BoxPlotDataPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BoxPlotDataPoint} BoxPlotDataPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BoxPlotDataPoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BoxPlotDataPoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.low = reader.double();
                        break;
                    }
                case 2: {
                        message.q1 = reader.double();
                        break;
                    }
                case 3: {
                        message.median = reader.double();
                        break;
                    }
                case 4: {
                        message.q3 = reader.double();
                        break;
                    }
                case 5: {
                        message.high = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BoxPlotDataPoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BoxPlotDataPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BoxPlotDataPoint} BoxPlotDataPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BoxPlotDataPoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BoxPlotDataPoint message.
         * @function verify
         * @memberof epoch_proto.BoxPlotDataPoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BoxPlotDataPoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.low != null && message.hasOwnProperty("low"))
                if (typeof message.low !== "number")
                    return "low: number expected";
            if (message.q1 != null && message.hasOwnProperty("q1"))
                if (typeof message.q1 !== "number")
                    return "q1: number expected";
            if (message.median != null && message.hasOwnProperty("median"))
                if (typeof message.median !== "number")
                    return "median: number expected";
            if (message.q3 != null && message.hasOwnProperty("q3"))
                if (typeof message.q3 !== "number")
                    return "q3: number expected";
            if (message.high != null && message.hasOwnProperty("high"))
                if (typeof message.high !== "number")
                    return "high: number expected";
            return null;
        };

        /**
         * Creates a BoxPlotDataPoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BoxPlotDataPoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BoxPlotDataPoint} BoxPlotDataPoint
         */
        BoxPlotDataPoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BoxPlotDataPoint)
                return object;
            let message = new $root.epoch_proto.BoxPlotDataPoint();
            if (object.low != null)
                message.low = Number(object.low);
            if (object.q1 != null)
                message.q1 = Number(object.q1);
            if (object.median != null)
                message.median = Number(object.median);
            if (object.q3 != null)
                message.q3 = Number(object.q3);
            if (object.high != null)
                message.high = Number(object.high);
            return message;
        };

        /**
         * Creates a plain object from a BoxPlotDataPoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BoxPlotDataPoint
         * @static
         * @param {epoch_proto.BoxPlotDataPoint} message BoxPlotDataPoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BoxPlotDataPoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.low = 0;
                object.q1 = 0;
                object.median = 0;
                object.q3 = 0;
                object.high = 0;
            }
            if (message.low != null && message.hasOwnProperty("low"))
                object.low = options.json && !isFinite(message.low) ? String(message.low) : message.low;
            if (message.q1 != null && message.hasOwnProperty("q1"))
                object.q1 = options.json && !isFinite(message.q1) ? String(message.q1) : message.q1;
            if (message.median != null && message.hasOwnProperty("median"))
                object.median = options.json && !isFinite(message.median) ? String(message.median) : message.median;
            if (message.q3 != null && message.hasOwnProperty("q3"))
                object.q3 = options.json && !isFinite(message.q3) ? String(message.q3) : message.q3;
            if (message.high != null && message.hasOwnProperty("high"))
                object.high = options.json && !isFinite(message.high) ? String(message.high) : message.high;
            return object;
        };

        /**
         * Converts this BoxPlotDataPoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.BoxPlotDataPoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BoxPlotDataPoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BoxPlotDataPoint
         * @function getTypeUrl
         * @memberof epoch_proto.BoxPlotDataPoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BoxPlotDataPoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BoxPlotDataPoint";
        };

        return BoxPlotDataPoint;
    })();

    epoch_proto.BoxPlotOutlier = (function() {

        /**
         * Properties of a BoxPlotOutlier.
         * @memberof epoch_proto
         * @interface IBoxPlotOutlier
         * @property {number|Long|null} [categoryIndex] BoxPlotOutlier categoryIndex
         * @property {number|null} [value] BoxPlotOutlier value
         */

        /**
         * Constructs a new BoxPlotOutlier.
         * @memberof epoch_proto
         * @classdesc Represents a BoxPlotOutlier.
         * @implements IBoxPlotOutlier
         * @constructor
         * @param {epoch_proto.IBoxPlotOutlier=} [properties] Properties to set
         */
        function BoxPlotOutlier(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BoxPlotOutlier categoryIndex.
         * @member {number|Long} categoryIndex
         * @memberof epoch_proto.BoxPlotOutlier
         * @instance
         */
        BoxPlotOutlier.prototype.categoryIndex = $util.Long ? $util.Long.fromBits(0,0,true) : 0;

        /**
         * BoxPlotOutlier value.
         * @member {number} value
         * @memberof epoch_proto.BoxPlotOutlier
         * @instance
         */
        BoxPlotOutlier.prototype.value = 0;

        /**
         * Creates a new BoxPlotOutlier instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BoxPlotOutlier
         * @static
         * @param {epoch_proto.IBoxPlotOutlier=} [properties] Properties to set
         * @returns {epoch_proto.BoxPlotOutlier} BoxPlotOutlier instance
         */
        BoxPlotOutlier.create = function create(properties) {
            return new BoxPlotOutlier(properties);
        };

        /**
         * Encodes the specified BoxPlotOutlier message. Does not implicitly {@link epoch_proto.BoxPlotOutlier.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BoxPlotOutlier
         * @static
         * @param {epoch_proto.IBoxPlotOutlier} message BoxPlotOutlier message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BoxPlotOutlier.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.categoryIndex != null && Object.hasOwnProperty.call(message, "categoryIndex"))
                writer.uint32(/* id 1, wireType 0 =*/8).uint64(message.categoryIndex);
            if (message.value != null && Object.hasOwnProperty.call(message, "value"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.value);
            return writer;
        };

        /**
         * Encodes the specified BoxPlotOutlier message, length delimited. Does not implicitly {@link epoch_proto.BoxPlotOutlier.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BoxPlotOutlier
         * @static
         * @param {epoch_proto.IBoxPlotOutlier} message BoxPlotOutlier message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BoxPlotOutlier.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BoxPlotOutlier message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BoxPlotOutlier
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BoxPlotOutlier} BoxPlotOutlier
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BoxPlotOutlier.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BoxPlotOutlier();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.categoryIndex = reader.uint64();
                        break;
                    }
                case 2: {
                        message.value = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BoxPlotOutlier message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BoxPlotOutlier
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BoxPlotOutlier} BoxPlotOutlier
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BoxPlotOutlier.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BoxPlotOutlier message.
         * @function verify
         * @memberof epoch_proto.BoxPlotOutlier
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BoxPlotOutlier.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.categoryIndex != null && message.hasOwnProperty("categoryIndex"))
                if (!$util.isInteger(message.categoryIndex) && !(message.categoryIndex && $util.isInteger(message.categoryIndex.low) && $util.isInteger(message.categoryIndex.high)))
                    return "categoryIndex: integer|Long expected";
            if (message.value != null && message.hasOwnProperty("value"))
                if (typeof message.value !== "number")
                    return "value: number expected";
            return null;
        };

        /**
         * Creates a BoxPlotOutlier message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BoxPlotOutlier
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BoxPlotOutlier} BoxPlotOutlier
         */
        BoxPlotOutlier.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BoxPlotOutlier)
                return object;
            let message = new $root.epoch_proto.BoxPlotOutlier();
            if (object.categoryIndex != null)
                if ($util.Long)
                    (message.categoryIndex = $util.Long.fromValue(object.categoryIndex)).unsigned = true;
                else if (typeof object.categoryIndex === "string")
                    message.categoryIndex = parseInt(object.categoryIndex, 10);
                else if (typeof object.categoryIndex === "number")
                    message.categoryIndex = object.categoryIndex;
                else if (typeof object.categoryIndex === "object")
                    message.categoryIndex = new $util.LongBits(object.categoryIndex.low >>> 0, object.categoryIndex.high >>> 0).toNumber(true);
            if (object.value != null)
                message.value = Number(object.value);
            return message;
        };

        /**
         * Creates a plain object from a BoxPlotOutlier message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BoxPlotOutlier
         * @static
         * @param {epoch_proto.BoxPlotOutlier} message BoxPlotOutlier
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BoxPlotOutlier.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                if ($util.Long) {
                    let long = new $util.Long(0, 0, true);
                    object.categoryIndex = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.categoryIndex = options.longs === String ? "0" : 0;
                object.value = 0;
            }
            if (message.categoryIndex != null && message.hasOwnProperty("categoryIndex"))
                if (typeof message.categoryIndex === "number")
                    object.categoryIndex = options.longs === String ? String(message.categoryIndex) : message.categoryIndex;
                else
                    object.categoryIndex = options.longs === String ? $util.Long.prototype.toString.call(message.categoryIndex) : options.longs === Number ? new $util.LongBits(message.categoryIndex.low >>> 0, message.categoryIndex.high >>> 0).toNumber(true) : message.categoryIndex;
            if (message.value != null && message.hasOwnProperty("value"))
                object.value = options.json && !isFinite(message.value) ? String(message.value) : message.value;
            return object;
        };

        /**
         * Converts this BoxPlotOutlier to JSON.
         * @function toJSON
         * @memberof epoch_proto.BoxPlotOutlier
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BoxPlotOutlier.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BoxPlotOutlier
         * @function getTypeUrl
         * @memberof epoch_proto.BoxPlotOutlier
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BoxPlotOutlier.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BoxPlotOutlier";
        };

        return BoxPlotOutlier;
    })();

    epoch_proto.BoxPlotDataPointDef = (function() {

        /**
         * Properties of a BoxPlotDataPointDef.
         * @memberof epoch_proto
         * @interface IBoxPlotDataPointDef
         * @property {Array.<epoch_proto.IBoxPlotOutlier>|null} [outliers] BoxPlotDataPointDef outliers
         * @property {Array.<epoch_proto.IBoxPlotDataPoint>|null} [points] BoxPlotDataPointDef points
         */

        /**
         * Constructs a new BoxPlotDataPointDef.
         * @memberof epoch_proto
         * @classdesc Represents a BoxPlotDataPointDef.
         * @implements IBoxPlotDataPointDef
         * @constructor
         * @param {epoch_proto.IBoxPlotDataPointDef=} [properties] Properties to set
         */
        function BoxPlotDataPointDef(properties) {
            this.outliers = [];
            this.points = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BoxPlotDataPointDef outliers.
         * @member {Array.<epoch_proto.IBoxPlotOutlier>} outliers
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @instance
         */
        BoxPlotDataPointDef.prototype.outliers = $util.emptyArray;

        /**
         * BoxPlotDataPointDef points.
         * @member {Array.<epoch_proto.IBoxPlotDataPoint>} points
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @instance
         */
        BoxPlotDataPointDef.prototype.points = $util.emptyArray;

        /**
         * Creates a new BoxPlotDataPointDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @static
         * @param {epoch_proto.IBoxPlotDataPointDef=} [properties] Properties to set
         * @returns {epoch_proto.BoxPlotDataPointDef} BoxPlotDataPointDef instance
         */
        BoxPlotDataPointDef.create = function create(properties) {
            return new BoxPlotDataPointDef(properties);
        };

        /**
         * Encodes the specified BoxPlotDataPointDef message. Does not implicitly {@link epoch_proto.BoxPlotDataPointDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @static
         * @param {epoch_proto.IBoxPlotDataPointDef} message BoxPlotDataPointDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BoxPlotDataPointDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.outliers != null && message.outliers.length)
                for (let i = 0; i < message.outliers.length; ++i)
                    $root.epoch_proto.BoxPlotOutlier.encode(message.outliers[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.points != null && message.points.length)
                for (let i = 0; i < message.points.length; ++i)
                    $root.epoch_proto.BoxPlotDataPoint.encode(message.points[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified BoxPlotDataPointDef message, length delimited. Does not implicitly {@link epoch_proto.BoxPlotDataPointDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @static
         * @param {epoch_proto.IBoxPlotDataPointDef} message BoxPlotDataPointDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BoxPlotDataPointDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BoxPlotDataPointDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BoxPlotDataPointDef} BoxPlotDataPointDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BoxPlotDataPointDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BoxPlotDataPointDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.outliers && message.outliers.length))
                            message.outliers = [];
                        message.outliers.push($root.epoch_proto.BoxPlotOutlier.decode(reader, reader.uint32()));
                        break;
                    }
                case 2: {
                        if (!(message.points && message.points.length))
                            message.points = [];
                        message.points.push($root.epoch_proto.BoxPlotDataPoint.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BoxPlotDataPointDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BoxPlotDataPointDef} BoxPlotDataPointDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BoxPlotDataPointDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BoxPlotDataPointDef message.
         * @function verify
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BoxPlotDataPointDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.outliers != null && message.hasOwnProperty("outliers")) {
                if (!Array.isArray(message.outliers))
                    return "outliers: array expected";
                for (let i = 0; i < message.outliers.length; ++i) {
                    let error = $root.epoch_proto.BoxPlotOutlier.verify(message.outliers[i]);
                    if (error)
                        return "outliers." + error;
                }
            }
            if (message.points != null && message.hasOwnProperty("points")) {
                if (!Array.isArray(message.points))
                    return "points: array expected";
                for (let i = 0; i < message.points.length; ++i) {
                    let error = $root.epoch_proto.BoxPlotDataPoint.verify(message.points[i]);
                    if (error)
                        return "points." + error;
                }
            }
            return null;
        };

        /**
         * Creates a BoxPlotDataPointDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BoxPlotDataPointDef} BoxPlotDataPointDef
         */
        BoxPlotDataPointDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BoxPlotDataPointDef)
                return object;
            let message = new $root.epoch_proto.BoxPlotDataPointDef();
            if (object.outliers) {
                if (!Array.isArray(object.outliers))
                    throw TypeError(".epoch_proto.BoxPlotDataPointDef.outliers: array expected");
                message.outliers = [];
                for (let i = 0; i < object.outliers.length; ++i) {
                    if (typeof object.outliers[i] !== "object")
                        throw TypeError(".epoch_proto.BoxPlotDataPointDef.outliers: object expected");
                    message.outliers[i] = $root.epoch_proto.BoxPlotOutlier.fromObject(object.outliers[i]);
                }
            }
            if (object.points) {
                if (!Array.isArray(object.points))
                    throw TypeError(".epoch_proto.BoxPlotDataPointDef.points: array expected");
                message.points = [];
                for (let i = 0; i < object.points.length; ++i) {
                    if (typeof object.points[i] !== "object")
                        throw TypeError(".epoch_proto.BoxPlotDataPointDef.points: object expected");
                    message.points[i] = $root.epoch_proto.BoxPlotDataPoint.fromObject(object.points[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a BoxPlotDataPointDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @static
         * @param {epoch_proto.BoxPlotDataPointDef} message BoxPlotDataPointDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BoxPlotDataPointDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults) {
                object.outliers = [];
                object.points = [];
            }
            if (message.outliers && message.outliers.length) {
                object.outliers = [];
                for (let j = 0; j < message.outliers.length; ++j)
                    object.outliers[j] = $root.epoch_proto.BoxPlotOutlier.toObject(message.outliers[j], options);
            }
            if (message.points && message.points.length) {
                object.points = [];
                for (let j = 0; j < message.points.length; ++j)
                    object.points[j] = $root.epoch_proto.BoxPlotDataPoint.toObject(message.points[j], options);
            }
            return object;
        };

        /**
         * Converts this BoxPlotDataPointDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BoxPlotDataPointDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BoxPlotDataPointDef
         * @function getTypeUrl
         * @memberof epoch_proto.BoxPlotDataPointDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BoxPlotDataPointDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BoxPlotDataPointDef";
        };

        return BoxPlotDataPointDef;
    })();

    epoch_proto.BoxPlotDef = (function() {

        /**
         * Properties of a BoxPlotDef.
         * @memberof epoch_proto
         * @interface IBoxPlotDef
         * @property {epoch_proto.IChartDef|null} [chartDef] BoxPlotDef chartDef
         * @property {epoch_proto.IBoxPlotDataPointDef|null} [data] BoxPlotDef data
         */

        /**
         * Constructs a new BoxPlotDef.
         * @memberof epoch_proto
         * @classdesc Represents a BoxPlotDef.
         * @implements IBoxPlotDef
         * @constructor
         * @param {epoch_proto.IBoxPlotDef=} [properties] Properties to set
         */
        function BoxPlotDef(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BoxPlotDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.BoxPlotDef
         * @instance
         */
        BoxPlotDef.prototype.chartDef = null;

        /**
         * BoxPlotDef data.
         * @member {epoch_proto.IBoxPlotDataPointDef|null|undefined} data
         * @memberof epoch_proto.BoxPlotDef
         * @instance
         */
        BoxPlotDef.prototype.data = null;

        /**
         * Creates a new BoxPlotDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BoxPlotDef
         * @static
         * @param {epoch_proto.IBoxPlotDef=} [properties] Properties to set
         * @returns {epoch_proto.BoxPlotDef} BoxPlotDef instance
         */
        BoxPlotDef.create = function create(properties) {
            return new BoxPlotDef(properties);
        };

        /**
         * Encodes the specified BoxPlotDef message. Does not implicitly {@link epoch_proto.BoxPlotDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BoxPlotDef
         * @static
         * @param {epoch_proto.IBoxPlotDef} message BoxPlotDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BoxPlotDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.data != null && Object.hasOwnProperty.call(message, "data"))
                $root.epoch_proto.BoxPlotDataPointDef.encode(message.data, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified BoxPlotDef message, length delimited. Does not implicitly {@link epoch_proto.BoxPlotDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BoxPlotDef
         * @static
         * @param {epoch_proto.IBoxPlotDef} message BoxPlotDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BoxPlotDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BoxPlotDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BoxPlotDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BoxPlotDef} BoxPlotDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BoxPlotDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BoxPlotDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        message.data = $root.epoch_proto.BoxPlotDataPointDef.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BoxPlotDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BoxPlotDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BoxPlotDef} BoxPlotDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BoxPlotDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BoxPlotDef message.
         * @function verify
         * @memberof epoch_proto.BoxPlotDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BoxPlotDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.data != null && message.hasOwnProperty("data")) {
                let error = $root.epoch_proto.BoxPlotDataPointDef.verify(message.data);
                if (error)
                    return "data." + error;
            }
            return null;
        };

        /**
         * Creates a BoxPlotDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BoxPlotDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BoxPlotDef} BoxPlotDef
         */
        BoxPlotDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BoxPlotDef)
                return object;
            let message = new $root.epoch_proto.BoxPlotDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.BoxPlotDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.data != null) {
                if (typeof object.data !== "object")
                    throw TypeError(".epoch_proto.BoxPlotDef.data: object expected");
                message.data = $root.epoch_proto.BoxPlotDataPointDef.fromObject(object.data);
            }
            return message;
        };

        /**
         * Creates a plain object from a BoxPlotDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BoxPlotDef
         * @static
         * @param {epoch_proto.BoxPlotDef} message BoxPlotDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BoxPlotDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.chartDef = null;
                object.data = null;
            }
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.data != null && message.hasOwnProperty("data"))
                object.data = $root.epoch_proto.BoxPlotDataPointDef.toObject(message.data, options);
            return object;
        };

        /**
         * Converts this BoxPlotDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.BoxPlotDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BoxPlotDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BoxPlotDef
         * @function getTypeUrl
         * @memberof epoch_proto.BoxPlotDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BoxPlotDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BoxPlotDef";
        };

        return BoxPlotDef;
    })();

    epoch_proto.XRangePoint = (function() {

        /**
         * Properties of a XRangePoint.
         * @memberof epoch_proto
         * @interface IXRangePoint
         * @property {number|Long|null} [x] XRangePoint x
         * @property {number|Long|null} [x2] XRangePoint x2
         * @property {number|Long|null} [y] XRangePoint y
         * @property {boolean|null} [isLong] XRangePoint isLong
         */

        /**
         * Constructs a new XRangePoint.
         * @memberof epoch_proto
         * @classdesc Represents a XRangePoint.
         * @implements IXRangePoint
         * @constructor
         * @param {epoch_proto.IXRangePoint=} [properties] Properties to set
         */
        function XRangePoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * XRangePoint x.
         * @member {number|Long} x
         * @memberof epoch_proto.XRangePoint
         * @instance
         */
        XRangePoint.prototype.x = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * XRangePoint x2.
         * @member {number|Long} x2
         * @memberof epoch_proto.XRangePoint
         * @instance
         */
        XRangePoint.prototype.x2 = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * XRangePoint y.
         * @member {number|Long} y
         * @memberof epoch_proto.XRangePoint
         * @instance
         */
        XRangePoint.prototype.y = $util.Long ? $util.Long.fromBits(0,0,true) : 0;

        /**
         * XRangePoint isLong.
         * @member {boolean} isLong
         * @memberof epoch_proto.XRangePoint
         * @instance
         */
        XRangePoint.prototype.isLong = false;

        /**
         * Creates a new XRangePoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.XRangePoint
         * @static
         * @param {epoch_proto.IXRangePoint=} [properties] Properties to set
         * @returns {epoch_proto.XRangePoint} XRangePoint instance
         */
        XRangePoint.create = function create(properties) {
            return new XRangePoint(properties);
        };

        /**
         * Encodes the specified XRangePoint message. Does not implicitly {@link epoch_proto.XRangePoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.XRangePoint
         * @static
         * @param {epoch_proto.IXRangePoint} message XRangePoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        XRangePoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 0 =*/8).int64(message.x);
            if (message.x2 != null && Object.hasOwnProperty.call(message, "x2"))
                writer.uint32(/* id 2, wireType 0 =*/16).int64(message.x2);
            if (message.y != null && Object.hasOwnProperty.call(message, "y"))
                writer.uint32(/* id 3, wireType 0 =*/24).uint64(message.y);
            if (message.isLong != null && Object.hasOwnProperty.call(message, "isLong"))
                writer.uint32(/* id 4, wireType 0 =*/32).bool(message.isLong);
            return writer;
        };

        /**
         * Encodes the specified XRangePoint message, length delimited. Does not implicitly {@link epoch_proto.XRangePoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.XRangePoint
         * @static
         * @param {epoch_proto.IXRangePoint} message XRangePoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        XRangePoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a XRangePoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.XRangePoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.XRangePoint} XRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        XRangePoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.XRangePoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.int64();
                        break;
                    }
                case 2: {
                        message.x2 = reader.int64();
                        break;
                    }
                case 3: {
                        message.y = reader.uint64();
                        break;
                    }
                case 4: {
                        message.isLong = reader.bool();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a XRangePoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.XRangePoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.XRangePoint} XRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        XRangePoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a XRangePoint message.
         * @function verify
         * @memberof epoch_proto.XRangePoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        XRangePoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.x != null && message.hasOwnProperty("x"))
                if (!$util.isInteger(message.x) && !(message.x && $util.isInteger(message.x.low) && $util.isInteger(message.x.high)))
                    return "x: integer|Long expected";
            if (message.x2 != null && message.hasOwnProperty("x2"))
                if (!$util.isInteger(message.x2) && !(message.x2 && $util.isInteger(message.x2.low) && $util.isInteger(message.x2.high)))
                    return "x2: integer|Long expected";
            if (message.y != null && message.hasOwnProperty("y"))
                if (!$util.isInteger(message.y) && !(message.y && $util.isInteger(message.y.low) && $util.isInteger(message.y.high)))
                    return "y: integer|Long expected";
            if (message.isLong != null && message.hasOwnProperty("isLong"))
                if (typeof message.isLong !== "boolean")
                    return "isLong: boolean expected";
            return null;
        };

        /**
         * Creates a XRangePoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.XRangePoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.XRangePoint} XRangePoint
         */
        XRangePoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.XRangePoint)
                return object;
            let message = new $root.epoch_proto.XRangePoint();
            if (object.x != null)
                if ($util.Long)
                    (message.x = $util.Long.fromValue(object.x)).unsigned = false;
                else if (typeof object.x === "string")
                    message.x = parseInt(object.x, 10);
                else if (typeof object.x === "number")
                    message.x = object.x;
                else if (typeof object.x === "object")
                    message.x = new $util.LongBits(object.x.low >>> 0, object.x.high >>> 0).toNumber();
            if (object.x2 != null)
                if ($util.Long)
                    (message.x2 = $util.Long.fromValue(object.x2)).unsigned = false;
                else if (typeof object.x2 === "string")
                    message.x2 = parseInt(object.x2, 10);
                else if (typeof object.x2 === "number")
                    message.x2 = object.x2;
                else if (typeof object.x2 === "object")
                    message.x2 = new $util.LongBits(object.x2.low >>> 0, object.x2.high >>> 0).toNumber();
            if (object.y != null)
                if ($util.Long)
                    (message.y = $util.Long.fromValue(object.y)).unsigned = true;
                else if (typeof object.y === "string")
                    message.y = parseInt(object.y, 10);
                else if (typeof object.y === "number")
                    message.y = object.y;
                else if (typeof object.y === "object")
                    message.y = new $util.LongBits(object.y.low >>> 0, object.y.high >>> 0).toNumber(true);
            if (object.isLong != null)
                message.isLong = Boolean(object.isLong);
            return message;
        };

        /**
         * Creates a plain object from a XRangePoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.XRangePoint
         * @static
         * @param {epoch_proto.XRangePoint} message XRangePoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        XRangePoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                if ($util.Long) {
                    let long = new $util.Long(0, 0, false);
                    object.x = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.x = options.longs === String ? "0" : 0;
                if ($util.Long) {
                    let long = new $util.Long(0, 0, false);
                    object.x2 = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.x2 = options.longs === String ? "0" : 0;
                if ($util.Long) {
                    let long = new $util.Long(0, 0, true);
                    object.y = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.y = options.longs === String ? "0" : 0;
                object.isLong = false;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x === "number")
                    object.x = options.longs === String ? String(message.x) : message.x;
                else
                    object.x = options.longs === String ? $util.Long.prototype.toString.call(message.x) : options.longs === Number ? new $util.LongBits(message.x.low >>> 0, message.x.high >>> 0).toNumber() : message.x;
            if (message.x2 != null && message.hasOwnProperty("x2"))
                if (typeof message.x2 === "number")
                    object.x2 = options.longs === String ? String(message.x2) : message.x2;
                else
                    object.x2 = options.longs === String ? $util.Long.prototype.toString.call(message.x2) : options.longs === Number ? new $util.LongBits(message.x2.low >>> 0, message.x2.high >>> 0).toNumber() : message.x2;
            if (message.y != null && message.hasOwnProperty("y"))
                if (typeof message.y === "number")
                    object.y = options.longs === String ? String(message.y) : message.y;
                else
                    object.y = options.longs === String ? $util.Long.prototype.toString.call(message.y) : options.longs === Number ? new $util.LongBits(message.y.low >>> 0, message.y.high >>> 0).toNumber(true) : message.y;
            if (message.isLong != null && message.hasOwnProperty("isLong"))
                object.isLong = message.isLong;
            return object;
        };

        /**
         * Converts this XRangePoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.XRangePoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        XRangePoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for XRangePoint
         * @function getTypeUrl
         * @memberof epoch_proto.XRangePoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        XRangePoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.XRangePoint";
        };

        return XRangePoint;
    })();

    epoch_proto.XRangeDef = (function() {

        /**
         * Properties of a XRangeDef.
         * @memberof epoch_proto
         * @interface IXRangeDef
         * @property {epoch_proto.IChartDef|null} [chartDef] XRangeDef chartDef
         * @property {Array.<string>|null} [categories] XRangeDef categories
         * @property {Array.<epoch_proto.IXRangePoint>|null} [points] XRangeDef points
         */

        /**
         * Constructs a new XRangeDef.
         * @memberof epoch_proto
         * @classdesc Represents a XRangeDef.
         * @implements IXRangeDef
         * @constructor
         * @param {epoch_proto.IXRangeDef=} [properties] Properties to set
         */
        function XRangeDef(properties) {
            this.categories = [];
            this.points = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * XRangeDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.XRangeDef
         * @instance
         */
        XRangeDef.prototype.chartDef = null;

        /**
         * XRangeDef categories.
         * @member {Array.<string>} categories
         * @memberof epoch_proto.XRangeDef
         * @instance
         */
        XRangeDef.prototype.categories = $util.emptyArray;

        /**
         * XRangeDef points.
         * @member {Array.<epoch_proto.IXRangePoint>} points
         * @memberof epoch_proto.XRangeDef
         * @instance
         */
        XRangeDef.prototype.points = $util.emptyArray;

        /**
         * Creates a new XRangeDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.XRangeDef
         * @static
         * @param {epoch_proto.IXRangeDef=} [properties] Properties to set
         * @returns {epoch_proto.XRangeDef} XRangeDef instance
         */
        XRangeDef.create = function create(properties) {
            return new XRangeDef(properties);
        };

        /**
         * Encodes the specified XRangeDef message. Does not implicitly {@link epoch_proto.XRangeDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.XRangeDef
         * @static
         * @param {epoch_proto.IXRangeDef} message XRangeDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        XRangeDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.categories != null && message.categories.length)
                for (let i = 0; i < message.categories.length; ++i)
                    writer.uint32(/* id 2, wireType 2 =*/18).string(message.categories[i]);
            if (message.points != null && message.points.length)
                for (let i = 0; i < message.points.length; ++i)
                    $root.epoch_proto.XRangePoint.encode(message.points[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified XRangeDef message, length delimited. Does not implicitly {@link epoch_proto.XRangeDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.XRangeDef
         * @static
         * @param {epoch_proto.IXRangeDef} message XRangeDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        XRangeDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a XRangeDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.XRangeDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.XRangeDef} XRangeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        XRangeDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.XRangeDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.categories && message.categories.length))
                            message.categories = [];
                        message.categories.push(reader.string());
                        break;
                    }
                case 3: {
                        if (!(message.points && message.points.length))
                            message.points = [];
                        message.points.push($root.epoch_proto.XRangePoint.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a XRangeDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.XRangeDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.XRangeDef} XRangeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        XRangeDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a XRangeDef message.
         * @function verify
         * @memberof epoch_proto.XRangeDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        XRangeDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.categories != null && message.hasOwnProperty("categories")) {
                if (!Array.isArray(message.categories))
                    return "categories: array expected";
                for (let i = 0; i < message.categories.length; ++i)
                    if (!$util.isString(message.categories[i]))
                        return "categories: string[] expected";
            }
            if (message.points != null && message.hasOwnProperty("points")) {
                if (!Array.isArray(message.points))
                    return "points: array expected";
                for (let i = 0; i < message.points.length; ++i) {
                    let error = $root.epoch_proto.XRangePoint.verify(message.points[i]);
                    if (error)
                        return "points." + error;
                }
            }
            return null;
        };

        /**
         * Creates a XRangeDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.XRangeDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.XRangeDef} XRangeDef
         */
        XRangeDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.XRangeDef)
                return object;
            let message = new $root.epoch_proto.XRangeDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.XRangeDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.categories) {
                if (!Array.isArray(object.categories))
                    throw TypeError(".epoch_proto.XRangeDef.categories: array expected");
                message.categories = [];
                for (let i = 0; i < object.categories.length; ++i)
                    message.categories[i] = String(object.categories[i]);
            }
            if (object.points) {
                if (!Array.isArray(object.points))
                    throw TypeError(".epoch_proto.XRangeDef.points: array expected");
                message.points = [];
                for (let i = 0; i < object.points.length; ++i) {
                    if (typeof object.points[i] !== "object")
                        throw TypeError(".epoch_proto.XRangeDef.points: object expected");
                    message.points[i] = $root.epoch_proto.XRangePoint.fromObject(object.points[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a XRangeDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.XRangeDef
         * @static
         * @param {epoch_proto.XRangeDef} message XRangeDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        XRangeDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults) {
                object.categories = [];
                object.points = [];
            }
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.categories && message.categories.length) {
                object.categories = [];
                for (let j = 0; j < message.categories.length; ++j)
                    object.categories[j] = message.categories[j];
            }
            if (message.points && message.points.length) {
                object.points = [];
                for (let j = 0; j < message.points.length; ++j)
                    object.points[j] = $root.epoch_proto.XRangePoint.toObject(message.points[j], options);
            }
            return object;
        };

        /**
         * Converts this XRangeDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.XRangeDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        XRangeDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for XRangeDef
         * @function getTypeUrl
         * @memberof epoch_proto.XRangeDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        XRangeDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.XRangeDef";
        };

        return XRangeDef;
    })();

    epoch_proto.PieData = (function() {

        /**
         * Properties of a PieData.
         * @memberof epoch_proto
         * @interface IPieData
         * @property {string|null} [name] PieData name
         * @property {number|null} [y] PieData y
         */

        /**
         * Constructs a new PieData.
         * @memberof epoch_proto
         * @classdesc Represents a PieData.
         * @implements IPieData
         * @constructor
         * @param {epoch_proto.IPieData=} [properties] Properties to set
         */
        function PieData(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * PieData name.
         * @member {string} name
         * @memberof epoch_proto.PieData
         * @instance
         */
        PieData.prototype.name = "";

        /**
         * PieData y.
         * @member {number} y
         * @memberof epoch_proto.PieData
         * @instance
         */
        PieData.prototype.y = 0;

        /**
         * Creates a new PieData instance using the specified properties.
         * @function create
         * @memberof epoch_proto.PieData
         * @static
         * @param {epoch_proto.IPieData=} [properties] Properties to set
         * @returns {epoch_proto.PieData} PieData instance
         */
        PieData.create = function create(properties) {
            return new PieData(properties);
        };

        /**
         * Encodes the specified PieData message. Does not implicitly {@link epoch_proto.PieData.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.PieData
         * @static
         * @param {epoch_proto.IPieData} message PieData message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        PieData.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.name);
            if (message.y != null && Object.hasOwnProperty.call(message, "y"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.y);
            return writer;
        };

        /**
         * Encodes the specified PieData message, length delimited. Does not implicitly {@link epoch_proto.PieData.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.PieData
         * @static
         * @param {epoch_proto.IPieData} message PieData message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        PieData.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a PieData message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.PieData
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.PieData} PieData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        PieData.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.PieData();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.name = reader.string();
                        break;
                    }
                case 2: {
                        message.y = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a PieData message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.PieData
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.PieData} PieData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        PieData.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a PieData message.
         * @function verify
         * @memberof epoch_proto.PieData
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        PieData.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.y != null && message.hasOwnProperty("y"))
                if (typeof message.y !== "number")
                    return "y: number expected";
            return null;
        };

        /**
         * Creates a PieData message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.PieData
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.PieData} PieData
         */
        PieData.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.PieData)
                return object;
            let message = new $root.epoch_proto.PieData();
            if (object.name != null)
                message.name = String(object.name);
            if (object.y != null)
                message.y = Number(object.y);
            return message;
        };

        /**
         * Creates a plain object from a PieData message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.PieData
         * @static
         * @param {epoch_proto.PieData} message PieData
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        PieData.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.name = "";
                object.y = 0;
            }
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.y != null && message.hasOwnProperty("y"))
                object.y = options.json && !isFinite(message.y) ? String(message.y) : message.y;
            return object;
        };

        /**
         * Converts this PieData to JSON.
         * @function toJSON
         * @memberof epoch_proto.PieData
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        PieData.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for PieData
         * @function getTypeUrl
         * @memberof epoch_proto.PieData
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        PieData.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.PieData";
        };

        return PieData;
    })();

    epoch_proto.PieDataDef = (function() {

        /**
         * Properties of a PieDataDef.
         * @memberof epoch_proto
         * @interface IPieDataDef
         * @property {string|null} [name] PieDataDef name
         * @property {Array.<epoch_proto.IPieData>|null} [points] PieDataDef points
         * @property {string|null} [size] PieDataDef size
         * @property {string|null} [innerSize] PieDataDef innerSize
         */

        /**
         * Constructs a new PieDataDef.
         * @memberof epoch_proto
         * @classdesc Represents a PieDataDef.
         * @implements IPieDataDef
         * @constructor
         * @param {epoch_proto.IPieDataDef=} [properties] Properties to set
         */
        function PieDataDef(properties) {
            this.points = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * PieDataDef name.
         * @member {string} name
         * @memberof epoch_proto.PieDataDef
         * @instance
         */
        PieDataDef.prototype.name = "";

        /**
         * PieDataDef points.
         * @member {Array.<epoch_proto.IPieData>} points
         * @memberof epoch_proto.PieDataDef
         * @instance
         */
        PieDataDef.prototype.points = $util.emptyArray;

        /**
         * PieDataDef size.
         * @member {string} size
         * @memberof epoch_proto.PieDataDef
         * @instance
         */
        PieDataDef.prototype.size = "";

        /**
         * PieDataDef innerSize.
         * @member {string|null|undefined} innerSize
         * @memberof epoch_proto.PieDataDef
         * @instance
         */
        PieDataDef.prototype.innerSize = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(PieDataDef.prototype, "_innerSize", {
            get: $util.oneOfGetter($oneOfFields = ["innerSize"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new PieDataDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.PieDataDef
         * @static
         * @param {epoch_proto.IPieDataDef=} [properties] Properties to set
         * @returns {epoch_proto.PieDataDef} PieDataDef instance
         */
        PieDataDef.create = function create(properties) {
            return new PieDataDef(properties);
        };

        /**
         * Encodes the specified PieDataDef message. Does not implicitly {@link epoch_proto.PieDataDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.PieDataDef
         * @static
         * @param {epoch_proto.IPieDataDef} message PieDataDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        PieDataDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.name);
            if (message.points != null && message.points.length)
                for (let i = 0; i < message.points.length; ++i)
                    $root.epoch_proto.PieData.encode(message.points[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.size != null && Object.hasOwnProperty.call(message, "size"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.size);
            if (message.innerSize != null && Object.hasOwnProperty.call(message, "innerSize"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.innerSize);
            return writer;
        };

        /**
         * Encodes the specified PieDataDef message, length delimited. Does not implicitly {@link epoch_proto.PieDataDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.PieDataDef
         * @static
         * @param {epoch_proto.IPieDataDef} message PieDataDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        PieDataDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a PieDataDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.PieDataDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.PieDataDef} PieDataDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        PieDataDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.PieDataDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.name = reader.string();
                        break;
                    }
                case 2: {
                        if (!(message.points && message.points.length))
                            message.points = [];
                        message.points.push($root.epoch_proto.PieData.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.size = reader.string();
                        break;
                    }
                case 4: {
                        message.innerSize = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a PieDataDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.PieDataDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.PieDataDef} PieDataDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        PieDataDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a PieDataDef message.
         * @function verify
         * @memberof epoch_proto.PieDataDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        PieDataDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.points != null && message.hasOwnProperty("points")) {
                if (!Array.isArray(message.points))
                    return "points: array expected";
                for (let i = 0; i < message.points.length; ++i) {
                    let error = $root.epoch_proto.PieData.verify(message.points[i]);
                    if (error)
                        return "points." + error;
                }
            }
            if (message.size != null && message.hasOwnProperty("size"))
                if (!$util.isString(message.size))
                    return "size: string expected";
            if (message.innerSize != null && message.hasOwnProperty("innerSize")) {
                properties._innerSize = 1;
                if (!$util.isString(message.innerSize))
                    return "innerSize: string expected";
            }
            return null;
        };

        /**
         * Creates a PieDataDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.PieDataDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.PieDataDef} PieDataDef
         */
        PieDataDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.PieDataDef)
                return object;
            let message = new $root.epoch_proto.PieDataDef();
            if (object.name != null)
                message.name = String(object.name);
            if (object.points) {
                if (!Array.isArray(object.points))
                    throw TypeError(".epoch_proto.PieDataDef.points: array expected");
                message.points = [];
                for (let i = 0; i < object.points.length; ++i) {
                    if (typeof object.points[i] !== "object")
                        throw TypeError(".epoch_proto.PieDataDef.points: object expected");
                    message.points[i] = $root.epoch_proto.PieData.fromObject(object.points[i]);
                }
            }
            if (object.size != null)
                message.size = String(object.size);
            if (object.innerSize != null)
                message.innerSize = String(object.innerSize);
            return message;
        };

        /**
         * Creates a plain object from a PieDataDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.PieDataDef
         * @static
         * @param {epoch_proto.PieDataDef} message PieDataDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        PieDataDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.points = [];
            if (options.defaults) {
                object.name = "";
                object.size = "";
            }
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.points && message.points.length) {
                object.points = [];
                for (let j = 0; j < message.points.length; ++j)
                    object.points[j] = $root.epoch_proto.PieData.toObject(message.points[j], options);
            }
            if (message.size != null && message.hasOwnProperty("size"))
                object.size = message.size;
            if (message.innerSize != null && message.hasOwnProperty("innerSize")) {
                object.innerSize = message.innerSize;
                if (options.oneofs)
                    object._innerSize = "innerSize";
            }
            return object;
        };

        /**
         * Converts this PieDataDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.PieDataDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        PieDataDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for PieDataDef
         * @function getTypeUrl
         * @memberof epoch_proto.PieDataDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        PieDataDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.PieDataDef";
        };

        return PieDataDef;
    })();

    epoch_proto.PieDef = (function() {

        /**
         * Properties of a PieDef.
         * @memberof epoch_proto
         * @interface IPieDef
         * @property {epoch_proto.IChartDef|null} [chartDef] PieDef chartDef
         * @property {Array.<epoch_proto.IPieDataDef>|null} [data] PieDef data
         */

        /**
         * Constructs a new PieDef.
         * @memberof epoch_proto
         * @classdesc Represents a PieDef.
         * @implements IPieDef
         * @constructor
         * @param {epoch_proto.IPieDef=} [properties] Properties to set
         */
        function PieDef(properties) {
            this.data = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * PieDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.PieDef
         * @instance
         */
        PieDef.prototype.chartDef = null;

        /**
         * PieDef data.
         * @member {Array.<epoch_proto.IPieDataDef>} data
         * @memberof epoch_proto.PieDef
         * @instance
         */
        PieDef.prototype.data = $util.emptyArray;

        /**
         * Creates a new PieDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.PieDef
         * @static
         * @param {epoch_proto.IPieDef=} [properties] Properties to set
         * @returns {epoch_proto.PieDef} PieDef instance
         */
        PieDef.create = function create(properties) {
            return new PieDef(properties);
        };

        /**
         * Encodes the specified PieDef message. Does not implicitly {@link epoch_proto.PieDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.PieDef
         * @static
         * @param {epoch_proto.IPieDef} message PieDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        PieDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.PieDataDef.encode(message.data[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified PieDef message, length delimited. Does not implicitly {@link epoch_proto.PieDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.PieDef
         * @static
         * @param {epoch_proto.IPieDef} message PieDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        PieDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a PieDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.PieDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.PieDef} PieDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        PieDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.PieDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.PieDataDef.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a PieDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.PieDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.PieDef} PieDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        PieDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a PieDef message.
         * @function verify
         * @memberof epoch_proto.PieDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        PieDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.PieDataDef.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            return null;
        };

        /**
         * Creates a PieDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.PieDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.PieDef} PieDef
         */
        PieDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.PieDef)
                return object;
            let message = new $root.epoch_proto.PieDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.PieDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.PieDef.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.PieDef.data: object expected");
                    message.data[i] = $root.epoch_proto.PieDataDef.fromObject(object.data[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a PieDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.PieDef
         * @static
         * @param {epoch_proto.PieDef} message PieDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        PieDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.data = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.PieDataDef.toObject(message.data[j], options);
            }
            return object;
        };

        /**
         * Converts this PieDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.PieDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        PieDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for PieDef
         * @function getTypeUrl
         * @memberof epoch_proto.PieDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        PieDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.PieDef";
        };

        return PieDef;
    })();

    epoch_proto.ScatterPoint = (function() {

        /**
         * Properties of a ScatterPoint.
         * @memberof epoch_proto
         * @interface IScatterPoint
         * @property {number|null} [x] ScatterPoint x
         * @property {number|null} [y] ScatterPoint y
         * @property {string|null} [name] ScatterPoint name
         * @property {string|null} [color] ScatterPoint color
         */

        /**
         * Constructs a new ScatterPoint.
         * @memberof epoch_proto
         * @classdesc Represents a ScatterPoint.
         * @implements IScatterPoint
         * @constructor
         * @param {epoch_proto.IScatterPoint=} [properties] Properties to set
         */
        function ScatterPoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ScatterPoint x.
         * @member {number} x
         * @memberof epoch_proto.ScatterPoint
         * @instance
         */
        ScatterPoint.prototype.x = 0;

        /**
         * ScatterPoint y.
         * @member {number} y
         * @memberof epoch_proto.ScatterPoint
         * @instance
         */
        ScatterPoint.prototype.y = 0;

        /**
         * ScatterPoint name.
         * @member {string|null|undefined} name
         * @memberof epoch_proto.ScatterPoint
         * @instance
         */
        ScatterPoint.prototype.name = null;

        /**
         * ScatterPoint color.
         * @member {string|null|undefined} color
         * @memberof epoch_proto.ScatterPoint
         * @instance
         */
        ScatterPoint.prototype.color = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(ScatterPoint.prototype, "_name", {
            get: $util.oneOfGetter($oneOfFields = ["name"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(ScatterPoint.prototype, "_color", {
            get: $util.oneOfGetter($oneOfFields = ["color"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new ScatterPoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.ScatterPoint
         * @static
         * @param {epoch_proto.IScatterPoint=} [properties] Properties to set
         * @returns {epoch_proto.ScatterPoint} ScatterPoint instance
         */
        ScatterPoint.create = function create(properties) {
            return new ScatterPoint(properties);
        };

        /**
         * Encodes the specified ScatterPoint message. Does not implicitly {@link epoch_proto.ScatterPoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.ScatterPoint
         * @static
         * @param {epoch_proto.IScatterPoint} message ScatterPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ScatterPoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 1 =*/9).double(message.x);
            if (message.y != null && Object.hasOwnProperty.call(message, "y"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.y);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.name);
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.color);
            return writer;
        };

        /**
         * Encodes the specified ScatterPoint message, length delimited. Does not implicitly {@link epoch_proto.ScatterPoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.ScatterPoint
         * @static
         * @param {epoch_proto.IScatterPoint} message ScatterPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ScatterPoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ScatterPoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.ScatterPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.ScatterPoint} ScatterPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ScatterPoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.ScatterPoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.double();
                        break;
                    }
                case 2: {
                        message.y = reader.double();
                        break;
                    }
                case 3: {
                        message.name = reader.string();
                        break;
                    }
                case 4: {
                        message.color = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ScatterPoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.ScatterPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.ScatterPoint} ScatterPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ScatterPoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ScatterPoint message.
         * @function verify
         * @memberof epoch_proto.ScatterPoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ScatterPoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x !== "number")
                    return "x: number expected";
            if (message.y != null && message.hasOwnProperty("y"))
                if (typeof message.y !== "number")
                    return "y: number expected";
            if (message.name != null && message.hasOwnProperty("name")) {
                properties._name = 1;
                if (!$util.isString(message.name))
                    return "name: string expected";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                properties._color = 1;
                if (!$util.isString(message.color))
                    return "color: string expected";
            }
            return null;
        };

        /**
         * Creates a ScatterPoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.ScatterPoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.ScatterPoint} ScatterPoint
         */
        ScatterPoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.ScatterPoint)
                return object;
            let message = new $root.epoch_proto.ScatterPoint();
            if (object.x != null)
                message.x = Number(object.x);
            if (object.y != null)
                message.y = Number(object.y);
            if (object.name != null)
                message.name = String(object.name);
            if (object.color != null)
                message.color = String(object.color);
            return message;
        };

        /**
         * Creates a plain object from a ScatterPoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.ScatterPoint
         * @static
         * @param {epoch_proto.ScatterPoint} message ScatterPoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ScatterPoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.x = 0;
                object.y = 0;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                object.x = options.json && !isFinite(message.x) ? String(message.x) : message.x;
            if (message.y != null && message.hasOwnProperty("y"))
                object.y = options.json && !isFinite(message.y) ? String(message.y) : message.y;
            if (message.name != null && message.hasOwnProperty("name")) {
                object.name = message.name;
                if (options.oneofs)
                    object._name = "name";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                object.color = message.color;
                if (options.oneofs)
                    object._color = "color";
            }
            return object;
        };

        /**
         * Converts this ScatterPoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.ScatterPoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ScatterPoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ScatterPoint
         * @function getTypeUrl
         * @memberof epoch_proto.ScatterPoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ScatterPoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.ScatterPoint";
        };

        return ScatterPoint;
    })();

    epoch_proto.ScatterSeries = (function() {

        /**
         * Properties of a ScatterSeries.
         * @memberof epoch_proto
         * @interface IScatterSeries
         * @property {string|null} [name] ScatterSeries name
         * @property {Array.<epoch_proto.IScatterPoint>|null} [data] ScatterSeries data
         * @property {string|null} [color] ScatterSeries color
         */

        /**
         * Constructs a new ScatterSeries.
         * @memberof epoch_proto
         * @classdesc Represents a ScatterSeries.
         * @implements IScatterSeries
         * @constructor
         * @param {epoch_proto.IScatterSeries=} [properties] Properties to set
         */
        function ScatterSeries(properties) {
            this.data = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ScatterSeries name.
         * @member {string} name
         * @memberof epoch_proto.ScatterSeries
         * @instance
         */
        ScatterSeries.prototype.name = "";

        /**
         * ScatterSeries data.
         * @member {Array.<epoch_proto.IScatterPoint>} data
         * @memberof epoch_proto.ScatterSeries
         * @instance
         */
        ScatterSeries.prototype.data = $util.emptyArray;

        /**
         * ScatterSeries color.
         * @member {string|null|undefined} color
         * @memberof epoch_proto.ScatterSeries
         * @instance
         */
        ScatterSeries.prototype.color = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(ScatterSeries.prototype, "_color", {
            get: $util.oneOfGetter($oneOfFields = ["color"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new ScatterSeries instance using the specified properties.
         * @function create
         * @memberof epoch_proto.ScatterSeries
         * @static
         * @param {epoch_proto.IScatterSeries=} [properties] Properties to set
         * @returns {epoch_proto.ScatterSeries} ScatterSeries instance
         */
        ScatterSeries.create = function create(properties) {
            return new ScatterSeries(properties);
        };

        /**
         * Encodes the specified ScatterSeries message. Does not implicitly {@link epoch_proto.ScatterSeries.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.ScatterSeries
         * @static
         * @param {epoch_proto.IScatterSeries} message ScatterSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ScatterSeries.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.name);
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.ScatterPoint.encode(message.data[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.color);
            return writer;
        };

        /**
         * Encodes the specified ScatterSeries message, length delimited. Does not implicitly {@link epoch_proto.ScatterSeries.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.ScatterSeries
         * @static
         * @param {epoch_proto.IScatterSeries} message ScatterSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ScatterSeries.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ScatterSeries message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.ScatterSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.ScatterSeries} ScatterSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ScatterSeries.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.ScatterSeries();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.name = reader.string();
                        break;
                    }
                case 2: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.ScatterPoint.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.color = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ScatterSeries message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.ScatterSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.ScatterSeries} ScatterSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ScatterSeries.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ScatterSeries message.
         * @function verify
         * @memberof epoch_proto.ScatterSeries
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ScatterSeries.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.ScatterPoint.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                properties._color = 1;
                if (!$util.isString(message.color))
                    return "color: string expected";
            }
            return null;
        };

        /**
         * Creates a ScatterSeries message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.ScatterSeries
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.ScatterSeries} ScatterSeries
         */
        ScatterSeries.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.ScatterSeries)
                return object;
            let message = new $root.epoch_proto.ScatterSeries();
            if (object.name != null)
                message.name = String(object.name);
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.ScatterSeries.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.ScatterSeries.data: object expected");
                    message.data[i] = $root.epoch_proto.ScatterPoint.fromObject(object.data[i]);
                }
            }
            if (object.color != null)
                message.color = String(object.color);
            return message;
        };

        /**
         * Creates a plain object from a ScatterSeries message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.ScatterSeries
         * @static
         * @param {epoch_proto.ScatterSeries} message ScatterSeries
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ScatterSeries.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.data = [];
            if (options.defaults)
                object.name = "";
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.ScatterPoint.toObject(message.data[j], options);
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                object.color = message.color;
                if (options.oneofs)
                    object._color = "color";
            }
            return object;
        };

        /**
         * Converts this ScatterSeries to JSON.
         * @function toJSON
         * @memberof epoch_proto.ScatterSeries
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ScatterSeries.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ScatterSeries
         * @function getTypeUrl
         * @memberof epoch_proto.ScatterSeries
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ScatterSeries.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.ScatterSeries";
        };

        return ScatterSeries;
    })();

    epoch_proto.ScatterDef = (function() {

        /**
         * Properties of a ScatterDef.
         * @memberof epoch_proto
         * @interface IScatterDef
         * @property {epoch_proto.IChartDef|null} [chartDef] ScatterDef chartDef
         * @property {Array.<epoch_proto.IScatterSeries>|null} [series] ScatterDef series
         * @property {Array.<epoch_proto.IStraightLineDef>|null} [straightLines] ScatterDef straightLines
         */

        /**
         * Constructs a new ScatterDef.
         * @memberof epoch_proto
         * @classdesc Represents a ScatterDef.
         * @implements IScatterDef
         * @constructor
         * @param {epoch_proto.IScatterDef=} [properties] Properties to set
         */
        function ScatterDef(properties) {
            this.series = [];
            this.straightLines = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ScatterDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.ScatterDef
         * @instance
         */
        ScatterDef.prototype.chartDef = null;

        /**
         * ScatterDef series.
         * @member {Array.<epoch_proto.IScatterSeries>} series
         * @memberof epoch_proto.ScatterDef
         * @instance
         */
        ScatterDef.prototype.series = $util.emptyArray;

        /**
         * ScatterDef straightLines.
         * @member {Array.<epoch_proto.IStraightLineDef>} straightLines
         * @memberof epoch_proto.ScatterDef
         * @instance
         */
        ScatterDef.prototype.straightLines = $util.emptyArray;

        /**
         * Creates a new ScatterDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.ScatterDef
         * @static
         * @param {epoch_proto.IScatterDef=} [properties] Properties to set
         * @returns {epoch_proto.ScatterDef} ScatterDef instance
         */
        ScatterDef.create = function create(properties) {
            return new ScatterDef(properties);
        };

        /**
         * Encodes the specified ScatterDef message. Does not implicitly {@link epoch_proto.ScatterDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.ScatterDef
         * @static
         * @param {epoch_proto.IScatterDef} message ScatterDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ScatterDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.series != null && message.series.length)
                for (let i = 0; i < message.series.length; ++i)
                    $root.epoch_proto.ScatterSeries.encode(message.series[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.straightLines != null && message.straightLines.length)
                for (let i = 0; i < message.straightLines.length; ++i)
                    $root.epoch_proto.StraightLineDef.encode(message.straightLines[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ScatterDef message, length delimited. Does not implicitly {@link epoch_proto.ScatterDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.ScatterDef
         * @static
         * @param {epoch_proto.IScatterDef} message ScatterDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ScatterDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ScatterDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.ScatterDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.ScatterDef} ScatterDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ScatterDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.ScatterDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.series && message.series.length))
                            message.series = [];
                        message.series.push($root.epoch_proto.ScatterSeries.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        if (!(message.straightLines && message.straightLines.length))
                            message.straightLines = [];
                        message.straightLines.push($root.epoch_proto.StraightLineDef.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ScatterDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.ScatterDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.ScatterDef} ScatterDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ScatterDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ScatterDef message.
         * @function verify
         * @memberof epoch_proto.ScatterDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ScatterDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.series != null && message.hasOwnProperty("series")) {
                if (!Array.isArray(message.series))
                    return "series: array expected";
                for (let i = 0; i < message.series.length; ++i) {
                    let error = $root.epoch_proto.ScatterSeries.verify(message.series[i]);
                    if (error)
                        return "series." + error;
                }
            }
            if (message.straightLines != null && message.hasOwnProperty("straightLines")) {
                if (!Array.isArray(message.straightLines))
                    return "straightLines: array expected";
                for (let i = 0; i < message.straightLines.length; ++i) {
                    let error = $root.epoch_proto.StraightLineDef.verify(message.straightLines[i]);
                    if (error)
                        return "straightLines." + error;
                }
            }
            return null;
        };

        /**
         * Creates a ScatterDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.ScatterDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.ScatterDef} ScatterDef
         */
        ScatterDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.ScatterDef)
                return object;
            let message = new $root.epoch_proto.ScatterDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.ScatterDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.series) {
                if (!Array.isArray(object.series))
                    throw TypeError(".epoch_proto.ScatterDef.series: array expected");
                message.series = [];
                for (let i = 0; i < object.series.length; ++i) {
                    if (typeof object.series[i] !== "object")
                        throw TypeError(".epoch_proto.ScatterDef.series: object expected");
                    message.series[i] = $root.epoch_proto.ScatterSeries.fromObject(object.series[i]);
                }
            }
            if (object.straightLines) {
                if (!Array.isArray(object.straightLines))
                    throw TypeError(".epoch_proto.ScatterDef.straightLines: array expected");
                message.straightLines = [];
                for (let i = 0; i < object.straightLines.length; ++i) {
                    if (typeof object.straightLines[i] !== "object")
                        throw TypeError(".epoch_proto.ScatterDef.straightLines: object expected");
                    message.straightLines[i] = $root.epoch_proto.StraightLineDef.fromObject(object.straightLines[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a ScatterDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.ScatterDef
         * @static
         * @param {epoch_proto.ScatterDef} message ScatterDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ScatterDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults) {
                object.series = [];
                object.straightLines = [];
            }
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.series && message.series.length) {
                object.series = [];
                for (let j = 0; j < message.series.length; ++j)
                    object.series[j] = $root.epoch_proto.ScatterSeries.toObject(message.series[j], options);
            }
            if (message.straightLines && message.straightLines.length) {
                object.straightLines = [];
                for (let j = 0; j < message.straightLines.length; ++j)
                    object.straightLines[j] = $root.epoch_proto.StraightLineDef.toObject(message.straightLines[j], options);
            }
            return object;
        };

        /**
         * Converts this ScatterDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.ScatterDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ScatterDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ScatterDef
         * @function getTypeUrl
         * @memberof epoch_proto.ScatterDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ScatterDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.ScatterDef";
        };

        return ScatterDef;
    })();

    epoch_proto.WaterfallPoint = (function() {

        /**
         * Properties of a WaterfallPoint.
         * @memberof epoch_proto
         * @interface IWaterfallPoint
         * @property {string|null} [name] WaterfallPoint name
         * @property {number|null} [y] WaterfallPoint y
         * @property {boolean|null} [isSum] WaterfallPoint isSum
         * @property {boolean|null} [isIntermediateSum] WaterfallPoint isIntermediateSum
         * @property {string|null} [color] WaterfallPoint color
         * @property {number|Long|null} [x] WaterfallPoint x
         */

        /**
         * Constructs a new WaterfallPoint.
         * @memberof epoch_proto
         * @classdesc Represents a WaterfallPoint.
         * @implements IWaterfallPoint
         * @constructor
         * @param {epoch_proto.IWaterfallPoint=} [properties] Properties to set
         */
        function WaterfallPoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * WaterfallPoint name.
         * @member {string} name
         * @memberof epoch_proto.WaterfallPoint
         * @instance
         */
        WaterfallPoint.prototype.name = "";

        /**
         * WaterfallPoint y.
         * @member {number} y
         * @memberof epoch_proto.WaterfallPoint
         * @instance
         */
        WaterfallPoint.prototype.y = 0;

        /**
         * WaterfallPoint isSum.
         * @member {boolean} isSum
         * @memberof epoch_proto.WaterfallPoint
         * @instance
         */
        WaterfallPoint.prototype.isSum = false;

        /**
         * WaterfallPoint isIntermediateSum.
         * @member {boolean} isIntermediateSum
         * @memberof epoch_proto.WaterfallPoint
         * @instance
         */
        WaterfallPoint.prototype.isIntermediateSum = false;

        /**
         * WaterfallPoint color.
         * @member {string|null|undefined} color
         * @memberof epoch_proto.WaterfallPoint
         * @instance
         */
        WaterfallPoint.prototype.color = null;

        /**
         * WaterfallPoint x.
         * @member {number|Long|null|undefined} x
         * @memberof epoch_proto.WaterfallPoint
         * @instance
         */
        WaterfallPoint.prototype.x = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(WaterfallPoint.prototype, "_color", {
            get: $util.oneOfGetter($oneOfFields = ["color"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(WaterfallPoint.prototype, "_x", {
            get: $util.oneOfGetter($oneOfFields = ["x"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new WaterfallPoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.WaterfallPoint
         * @static
         * @param {epoch_proto.IWaterfallPoint=} [properties] Properties to set
         * @returns {epoch_proto.WaterfallPoint} WaterfallPoint instance
         */
        WaterfallPoint.create = function create(properties) {
            return new WaterfallPoint(properties);
        };

        /**
         * Encodes the specified WaterfallPoint message. Does not implicitly {@link epoch_proto.WaterfallPoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.WaterfallPoint
         * @static
         * @param {epoch_proto.IWaterfallPoint} message WaterfallPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        WaterfallPoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.name);
            if (message.y != null && Object.hasOwnProperty.call(message, "y"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.y);
            if (message.isSum != null && Object.hasOwnProperty.call(message, "isSum"))
                writer.uint32(/* id 3, wireType 0 =*/24).bool(message.isSum);
            if (message.isIntermediateSum != null && Object.hasOwnProperty.call(message, "isIntermediateSum"))
                writer.uint32(/* id 4, wireType 0 =*/32).bool(message.isIntermediateSum);
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.color);
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 6, wireType 0 =*/48).int64(message.x);
            return writer;
        };

        /**
         * Encodes the specified WaterfallPoint message, length delimited. Does not implicitly {@link epoch_proto.WaterfallPoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.WaterfallPoint
         * @static
         * @param {epoch_proto.IWaterfallPoint} message WaterfallPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        WaterfallPoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a WaterfallPoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.WaterfallPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.WaterfallPoint} WaterfallPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        WaterfallPoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.WaterfallPoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.name = reader.string();
                        break;
                    }
                case 2: {
                        message.y = reader.double();
                        break;
                    }
                case 3: {
                        message.isSum = reader.bool();
                        break;
                    }
                case 4: {
                        message.isIntermediateSum = reader.bool();
                        break;
                    }
                case 5: {
                        message.color = reader.string();
                        break;
                    }
                case 6: {
                        message.x = reader.int64();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a WaterfallPoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.WaterfallPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.WaterfallPoint} WaterfallPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        WaterfallPoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a WaterfallPoint message.
         * @function verify
         * @memberof epoch_proto.WaterfallPoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        WaterfallPoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.y != null && message.hasOwnProperty("y"))
                if (typeof message.y !== "number")
                    return "y: number expected";
            if (message.isSum != null && message.hasOwnProperty("isSum"))
                if (typeof message.isSum !== "boolean")
                    return "isSum: boolean expected";
            if (message.isIntermediateSum != null && message.hasOwnProperty("isIntermediateSum"))
                if (typeof message.isIntermediateSum !== "boolean")
                    return "isIntermediateSum: boolean expected";
            if (message.color != null && message.hasOwnProperty("color")) {
                properties._color = 1;
                if (!$util.isString(message.color))
                    return "color: string expected";
            }
            if (message.x != null && message.hasOwnProperty("x")) {
                properties._x = 1;
                if (!$util.isInteger(message.x) && !(message.x && $util.isInteger(message.x.low) && $util.isInteger(message.x.high)))
                    return "x: integer|Long expected";
            }
            return null;
        };

        /**
         * Creates a WaterfallPoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.WaterfallPoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.WaterfallPoint} WaterfallPoint
         */
        WaterfallPoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.WaterfallPoint)
                return object;
            let message = new $root.epoch_proto.WaterfallPoint();
            if (object.name != null)
                message.name = String(object.name);
            if (object.y != null)
                message.y = Number(object.y);
            if (object.isSum != null)
                message.isSum = Boolean(object.isSum);
            if (object.isIntermediateSum != null)
                message.isIntermediateSum = Boolean(object.isIntermediateSum);
            if (object.color != null)
                message.color = String(object.color);
            if (object.x != null)
                if ($util.Long)
                    (message.x = $util.Long.fromValue(object.x)).unsigned = false;
                else if (typeof object.x === "string")
                    message.x = parseInt(object.x, 10);
                else if (typeof object.x === "number")
                    message.x = object.x;
                else if (typeof object.x === "object")
                    message.x = new $util.LongBits(object.x.low >>> 0, object.x.high >>> 0).toNumber();
            return message;
        };

        /**
         * Creates a plain object from a WaterfallPoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.WaterfallPoint
         * @static
         * @param {epoch_proto.WaterfallPoint} message WaterfallPoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        WaterfallPoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.name = "";
                object.y = 0;
                object.isSum = false;
                object.isIntermediateSum = false;
            }
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.y != null && message.hasOwnProperty("y"))
                object.y = options.json && !isFinite(message.y) ? String(message.y) : message.y;
            if (message.isSum != null && message.hasOwnProperty("isSum"))
                object.isSum = message.isSum;
            if (message.isIntermediateSum != null && message.hasOwnProperty("isIntermediateSum"))
                object.isIntermediateSum = message.isIntermediateSum;
            if (message.color != null && message.hasOwnProperty("color")) {
                object.color = message.color;
                if (options.oneofs)
                    object._color = "color";
            }
            if (message.x != null && message.hasOwnProperty("x")) {
                if (typeof message.x === "number")
                    object.x = options.longs === String ? String(message.x) : message.x;
                else
                    object.x = options.longs === String ? $util.Long.prototype.toString.call(message.x) : options.longs === Number ? new $util.LongBits(message.x.low >>> 0, message.x.high >>> 0).toNumber() : message.x;
                if (options.oneofs)
                    object._x = "x";
            }
            return object;
        };

        /**
         * Converts this WaterfallPoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.WaterfallPoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        WaterfallPoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for WaterfallPoint
         * @function getTypeUrl
         * @memberof epoch_proto.WaterfallPoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        WaterfallPoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.WaterfallPoint";
        };

        return WaterfallPoint;
    })();

    epoch_proto.WaterfallDef = (function() {

        /**
         * Properties of a WaterfallDef.
         * @memberof epoch_proto
         * @interface IWaterfallDef
         * @property {epoch_proto.IChartDef|null} [chartDef] WaterfallDef chartDef
         * @property {Array.<epoch_proto.IWaterfallPoint>|null} [points] WaterfallDef points
         * @property {string|null} [upColor] WaterfallDef upColor
         * @property {string|null} [downColor] WaterfallDef downColor
         * @property {string|null} [sumColor] WaterfallDef sumColor
         */

        /**
         * Constructs a new WaterfallDef.
         * @memberof epoch_proto
         * @classdesc Represents a WaterfallDef.
         * @implements IWaterfallDef
         * @constructor
         * @param {epoch_proto.IWaterfallDef=} [properties] Properties to set
         */
        function WaterfallDef(properties) {
            this.points = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * WaterfallDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.WaterfallDef
         * @instance
         */
        WaterfallDef.prototype.chartDef = null;

        /**
         * WaterfallDef points.
         * @member {Array.<epoch_proto.IWaterfallPoint>} points
         * @memberof epoch_proto.WaterfallDef
         * @instance
         */
        WaterfallDef.prototype.points = $util.emptyArray;

        /**
         * WaterfallDef upColor.
         * @member {string|null|undefined} upColor
         * @memberof epoch_proto.WaterfallDef
         * @instance
         */
        WaterfallDef.prototype.upColor = null;

        /**
         * WaterfallDef downColor.
         * @member {string|null|undefined} downColor
         * @memberof epoch_proto.WaterfallDef
         * @instance
         */
        WaterfallDef.prototype.downColor = null;

        /**
         * WaterfallDef sumColor.
         * @member {string|null|undefined} sumColor
         * @memberof epoch_proto.WaterfallDef
         * @instance
         */
        WaterfallDef.prototype.sumColor = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(WaterfallDef.prototype, "_upColor", {
            get: $util.oneOfGetter($oneOfFields = ["upColor"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(WaterfallDef.prototype, "_downColor", {
            get: $util.oneOfGetter($oneOfFields = ["downColor"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(WaterfallDef.prototype, "_sumColor", {
            get: $util.oneOfGetter($oneOfFields = ["sumColor"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new WaterfallDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.WaterfallDef
         * @static
         * @param {epoch_proto.IWaterfallDef=} [properties] Properties to set
         * @returns {epoch_proto.WaterfallDef} WaterfallDef instance
         */
        WaterfallDef.create = function create(properties) {
            return new WaterfallDef(properties);
        };

        /**
         * Encodes the specified WaterfallDef message. Does not implicitly {@link epoch_proto.WaterfallDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.WaterfallDef
         * @static
         * @param {epoch_proto.IWaterfallDef} message WaterfallDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        WaterfallDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.points != null && message.points.length)
                for (let i = 0; i < message.points.length; ++i)
                    $root.epoch_proto.WaterfallPoint.encode(message.points[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.upColor != null && Object.hasOwnProperty.call(message, "upColor"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.upColor);
            if (message.downColor != null && Object.hasOwnProperty.call(message, "downColor"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.downColor);
            if (message.sumColor != null && Object.hasOwnProperty.call(message, "sumColor"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.sumColor);
            return writer;
        };

        /**
         * Encodes the specified WaterfallDef message, length delimited. Does not implicitly {@link epoch_proto.WaterfallDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.WaterfallDef
         * @static
         * @param {epoch_proto.IWaterfallDef} message WaterfallDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        WaterfallDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a WaterfallDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.WaterfallDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.WaterfallDef} WaterfallDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        WaterfallDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.WaterfallDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.points && message.points.length))
                            message.points = [];
                        message.points.push($root.epoch_proto.WaterfallPoint.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.upColor = reader.string();
                        break;
                    }
                case 4: {
                        message.downColor = reader.string();
                        break;
                    }
                case 5: {
                        message.sumColor = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a WaterfallDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.WaterfallDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.WaterfallDef} WaterfallDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        WaterfallDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a WaterfallDef message.
         * @function verify
         * @memberof epoch_proto.WaterfallDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        WaterfallDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.points != null && message.hasOwnProperty("points")) {
                if (!Array.isArray(message.points))
                    return "points: array expected";
                for (let i = 0; i < message.points.length; ++i) {
                    let error = $root.epoch_proto.WaterfallPoint.verify(message.points[i]);
                    if (error)
                        return "points." + error;
                }
            }
            if (message.upColor != null && message.hasOwnProperty("upColor")) {
                properties._upColor = 1;
                if (!$util.isString(message.upColor))
                    return "upColor: string expected";
            }
            if (message.downColor != null && message.hasOwnProperty("downColor")) {
                properties._downColor = 1;
                if (!$util.isString(message.downColor))
                    return "downColor: string expected";
            }
            if (message.sumColor != null && message.hasOwnProperty("sumColor")) {
                properties._sumColor = 1;
                if (!$util.isString(message.sumColor))
                    return "sumColor: string expected";
            }
            return null;
        };

        /**
         * Creates a WaterfallDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.WaterfallDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.WaterfallDef} WaterfallDef
         */
        WaterfallDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.WaterfallDef)
                return object;
            let message = new $root.epoch_proto.WaterfallDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.WaterfallDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.points) {
                if (!Array.isArray(object.points))
                    throw TypeError(".epoch_proto.WaterfallDef.points: array expected");
                message.points = [];
                for (let i = 0; i < object.points.length; ++i) {
                    if (typeof object.points[i] !== "object")
                        throw TypeError(".epoch_proto.WaterfallDef.points: object expected");
                    message.points[i] = $root.epoch_proto.WaterfallPoint.fromObject(object.points[i]);
                }
            }
            if (object.upColor != null)
                message.upColor = String(object.upColor);
            if (object.downColor != null)
                message.downColor = String(object.downColor);
            if (object.sumColor != null)
                message.sumColor = String(object.sumColor);
            return message;
        };

        /**
         * Creates a plain object from a WaterfallDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.WaterfallDef
         * @static
         * @param {epoch_proto.WaterfallDef} message WaterfallDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        WaterfallDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.points = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.points && message.points.length) {
                object.points = [];
                for (let j = 0; j < message.points.length; ++j)
                    object.points[j] = $root.epoch_proto.WaterfallPoint.toObject(message.points[j], options);
            }
            if (message.upColor != null && message.hasOwnProperty("upColor")) {
                object.upColor = message.upColor;
                if (options.oneofs)
                    object._upColor = "upColor";
            }
            if (message.downColor != null && message.hasOwnProperty("downColor")) {
                object.downColor = message.downColor;
                if (options.oneofs)
                    object._downColor = "downColor";
            }
            if (message.sumColor != null && message.hasOwnProperty("sumColor")) {
                object.sumColor = message.sumColor;
                if (options.oneofs)
                    object._sumColor = "sumColor";
            }
            return object;
        };

        /**
         * Converts this WaterfallDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.WaterfallDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        WaterfallDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for WaterfallDef
         * @function getTypeUrl
         * @memberof epoch_proto.WaterfallDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        WaterfallDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.WaterfallDef";
        };

        return WaterfallDef;
    })();

    epoch_proto.SplineDef = (function() {

        /**
         * Properties of a SplineDef.
         * @memberof epoch_proto
         * @interface ISplineDef
         * @property {epoch_proto.IChartDef|null} [chartDef] SplineDef chartDef
         * @property {Array.<epoch_proto.ILine>|null} [lines] SplineDef lines
         * @property {Array.<epoch_proto.IStraightLineDef>|null} [straightLines] SplineDef straightLines
         * @property {Array.<epoch_proto.IBand>|null} [yPlotBands] SplineDef yPlotBands
         * @property {epoch_proto.ILine|null} [overlay] SplineDef overlay
         */

        /**
         * Constructs a new SplineDef.
         * @memberof epoch_proto
         * @classdesc Represents a SplineDef.
         * @implements ISplineDef
         * @constructor
         * @param {epoch_proto.ISplineDef=} [properties] Properties to set
         */
        function SplineDef(properties) {
            this.lines = [];
            this.straightLines = [];
            this.yPlotBands = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * SplineDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.SplineDef
         * @instance
         */
        SplineDef.prototype.chartDef = null;

        /**
         * SplineDef lines.
         * @member {Array.<epoch_proto.ILine>} lines
         * @memberof epoch_proto.SplineDef
         * @instance
         */
        SplineDef.prototype.lines = $util.emptyArray;

        /**
         * SplineDef straightLines.
         * @member {Array.<epoch_proto.IStraightLineDef>} straightLines
         * @memberof epoch_proto.SplineDef
         * @instance
         */
        SplineDef.prototype.straightLines = $util.emptyArray;

        /**
         * SplineDef yPlotBands.
         * @member {Array.<epoch_proto.IBand>} yPlotBands
         * @memberof epoch_proto.SplineDef
         * @instance
         */
        SplineDef.prototype.yPlotBands = $util.emptyArray;

        /**
         * SplineDef overlay.
         * @member {epoch_proto.ILine|null|undefined} overlay
         * @memberof epoch_proto.SplineDef
         * @instance
         */
        SplineDef.prototype.overlay = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(SplineDef.prototype, "_overlay", {
            get: $util.oneOfGetter($oneOfFields = ["overlay"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new SplineDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.SplineDef
         * @static
         * @param {epoch_proto.ISplineDef=} [properties] Properties to set
         * @returns {epoch_proto.SplineDef} SplineDef instance
         */
        SplineDef.create = function create(properties) {
            return new SplineDef(properties);
        };

        /**
         * Encodes the specified SplineDef message. Does not implicitly {@link epoch_proto.SplineDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.SplineDef
         * @static
         * @param {epoch_proto.ISplineDef} message SplineDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SplineDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.lines != null && message.lines.length)
                for (let i = 0; i < message.lines.length; ++i)
                    $root.epoch_proto.Line.encode(message.lines[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.straightLines != null && message.straightLines.length)
                for (let i = 0; i < message.straightLines.length; ++i)
                    $root.epoch_proto.StraightLineDef.encode(message.straightLines[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.yPlotBands != null && message.yPlotBands.length)
                for (let i = 0; i < message.yPlotBands.length; ++i)
                    $root.epoch_proto.Band.encode(message.yPlotBands[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
            if (message.overlay != null && Object.hasOwnProperty.call(message, "overlay"))
                $root.epoch_proto.Line.encode(message.overlay, writer.uint32(/* id 5, wireType 2 =*/42).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified SplineDef message, length delimited. Does not implicitly {@link epoch_proto.SplineDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.SplineDef
         * @static
         * @param {epoch_proto.ISplineDef} message SplineDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SplineDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a SplineDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.SplineDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.SplineDef} SplineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SplineDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.SplineDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.lines && message.lines.length))
                            message.lines = [];
                        message.lines.push($root.epoch_proto.Line.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        if (!(message.straightLines && message.straightLines.length))
                            message.straightLines = [];
                        message.straightLines.push($root.epoch_proto.StraightLineDef.decode(reader, reader.uint32()));
                        break;
                    }
                case 4: {
                        if (!(message.yPlotBands && message.yPlotBands.length))
                            message.yPlotBands = [];
                        message.yPlotBands.push($root.epoch_proto.Band.decode(reader, reader.uint32()));
                        break;
                    }
                case 5: {
                        message.overlay = $root.epoch_proto.Line.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a SplineDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.SplineDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.SplineDef} SplineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SplineDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a SplineDef message.
         * @function verify
         * @memberof epoch_proto.SplineDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        SplineDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.lines != null && message.hasOwnProperty("lines")) {
                if (!Array.isArray(message.lines))
                    return "lines: array expected";
                for (let i = 0; i < message.lines.length; ++i) {
                    let error = $root.epoch_proto.Line.verify(message.lines[i]);
                    if (error)
                        return "lines." + error;
                }
            }
            if (message.straightLines != null && message.hasOwnProperty("straightLines")) {
                if (!Array.isArray(message.straightLines))
                    return "straightLines: array expected";
                for (let i = 0; i < message.straightLines.length; ++i) {
                    let error = $root.epoch_proto.StraightLineDef.verify(message.straightLines[i]);
                    if (error)
                        return "straightLines." + error;
                }
            }
            if (message.yPlotBands != null && message.hasOwnProperty("yPlotBands")) {
                if (!Array.isArray(message.yPlotBands))
                    return "yPlotBands: array expected";
                for (let i = 0; i < message.yPlotBands.length; ++i) {
                    let error = $root.epoch_proto.Band.verify(message.yPlotBands[i]);
                    if (error)
                        return "yPlotBands." + error;
                }
            }
            if (message.overlay != null && message.hasOwnProperty("overlay")) {
                properties._overlay = 1;
                {
                    let error = $root.epoch_proto.Line.verify(message.overlay);
                    if (error)
                        return "overlay." + error;
                }
            }
            return null;
        };

        /**
         * Creates a SplineDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.SplineDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.SplineDef} SplineDef
         */
        SplineDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.SplineDef)
                return object;
            let message = new $root.epoch_proto.SplineDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.SplineDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.lines) {
                if (!Array.isArray(object.lines))
                    throw TypeError(".epoch_proto.SplineDef.lines: array expected");
                message.lines = [];
                for (let i = 0; i < object.lines.length; ++i) {
                    if (typeof object.lines[i] !== "object")
                        throw TypeError(".epoch_proto.SplineDef.lines: object expected");
                    message.lines[i] = $root.epoch_proto.Line.fromObject(object.lines[i]);
                }
            }
            if (object.straightLines) {
                if (!Array.isArray(object.straightLines))
                    throw TypeError(".epoch_proto.SplineDef.straightLines: array expected");
                message.straightLines = [];
                for (let i = 0; i < object.straightLines.length; ++i) {
                    if (typeof object.straightLines[i] !== "object")
                        throw TypeError(".epoch_proto.SplineDef.straightLines: object expected");
                    message.straightLines[i] = $root.epoch_proto.StraightLineDef.fromObject(object.straightLines[i]);
                }
            }
            if (object.yPlotBands) {
                if (!Array.isArray(object.yPlotBands))
                    throw TypeError(".epoch_proto.SplineDef.yPlotBands: array expected");
                message.yPlotBands = [];
                for (let i = 0; i < object.yPlotBands.length; ++i) {
                    if (typeof object.yPlotBands[i] !== "object")
                        throw TypeError(".epoch_proto.SplineDef.yPlotBands: object expected");
                    message.yPlotBands[i] = $root.epoch_proto.Band.fromObject(object.yPlotBands[i]);
                }
            }
            if (object.overlay != null) {
                if (typeof object.overlay !== "object")
                    throw TypeError(".epoch_proto.SplineDef.overlay: object expected");
                message.overlay = $root.epoch_proto.Line.fromObject(object.overlay);
            }
            return message;
        };

        /**
         * Creates a plain object from a SplineDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.SplineDef
         * @static
         * @param {epoch_proto.SplineDef} message SplineDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        SplineDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults) {
                object.lines = [];
                object.straightLines = [];
                object.yPlotBands = [];
            }
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.lines && message.lines.length) {
                object.lines = [];
                for (let j = 0; j < message.lines.length; ++j)
                    object.lines[j] = $root.epoch_proto.Line.toObject(message.lines[j], options);
            }
            if (message.straightLines && message.straightLines.length) {
                object.straightLines = [];
                for (let j = 0; j < message.straightLines.length; ++j)
                    object.straightLines[j] = $root.epoch_proto.StraightLineDef.toObject(message.straightLines[j], options);
            }
            if (message.yPlotBands && message.yPlotBands.length) {
                object.yPlotBands = [];
                for (let j = 0; j < message.yPlotBands.length; ++j)
                    object.yPlotBands[j] = $root.epoch_proto.Band.toObject(message.yPlotBands[j], options);
            }
            if (message.overlay != null && message.hasOwnProperty("overlay")) {
                object.overlay = $root.epoch_proto.Line.toObject(message.overlay, options);
                if (options.oneofs)
                    object._overlay = "overlay";
            }
            return object;
        };

        /**
         * Converts this SplineDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.SplineDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        SplineDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for SplineDef
         * @function getTypeUrl
         * @memberof epoch_proto.SplineDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        SplineDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.SplineDef";
        };

        return SplineDef;
    })();

    epoch_proto.NumericSplineDef = (function() {

        /**
         * Properties of a NumericSplineDef.
         * @memberof epoch_proto
         * @interface INumericSplineDef
         * @property {epoch_proto.IChartDef|null} [chartDef] NumericSplineDef chartDef
         * @property {Array.<epoch_proto.INumericLine>|null} [lines] NumericSplineDef lines
         * @property {Array.<epoch_proto.IStraightLineDef>|null} [straightLines] NumericSplineDef straightLines
         * @property {Array.<epoch_proto.IBand>|null} [yPlotBands] NumericSplineDef yPlotBands
         */

        /**
         * Constructs a new NumericSplineDef.
         * @memberof epoch_proto
         * @classdesc Represents a NumericSplineDef.
         * @implements INumericSplineDef
         * @constructor
         * @param {epoch_proto.INumericSplineDef=} [properties] Properties to set
         */
        function NumericSplineDef(properties) {
            this.lines = [];
            this.straightLines = [];
            this.yPlotBands = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NumericSplineDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.NumericSplineDef
         * @instance
         */
        NumericSplineDef.prototype.chartDef = null;

        /**
         * NumericSplineDef lines.
         * @member {Array.<epoch_proto.INumericLine>} lines
         * @memberof epoch_proto.NumericSplineDef
         * @instance
         */
        NumericSplineDef.prototype.lines = $util.emptyArray;

        /**
         * NumericSplineDef straightLines.
         * @member {Array.<epoch_proto.IStraightLineDef>} straightLines
         * @memberof epoch_proto.NumericSplineDef
         * @instance
         */
        NumericSplineDef.prototype.straightLines = $util.emptyArray;

        /**
         * NumericSplineDef yPlotBands.
         * @member {Array.<epoch_proto.IBand>} yPlotBands
         * @memberof epoch_proto.NumericSplineDef
         * @instance
         */
        NumericSplineDef.prototype.yPlotBands = $util.emptyArray;

        /**
         * Creates a new NumericSplineDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.NumericSplineDef
         * @static
         * @param {epoch_proto.INumericSplineDef=} [properties] Properties to set
         * @returns {epoch_proto.NumericSplineDef} NumericSplineDef instance
         */
        NumericSplineDef.create = function create(properties) {
            return new NumericSplineDef(properties);
        };

        /**
         * Encodes the specified NumericSplineDef message. Does not implicitly {@link epoch_proto.NumericSplineDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.NumericSplineDef
         * @static
         * @param {epoch_proto.INumericSplineDef} message NumericSplineDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericSplineDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.lines != null && message.lines.length)
                for (let i = 0; i < message.lines.length; ++i)
                    $root.epoch_proto.NumericLine.encode(message.lines[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.straightLines != null && message.straightLines.length)
                for (let i = 0; i < message.straightLines.length; ++i)
                    $root.epoch_proto.StraightLineDef.encode(message.straightLines[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.yPlotBands != null && message.yPlotBands.length)
                for (let i = 0; i < message.yPlotBands.length; ++i)
                    $root.epoch_proto.Band.encode(message.yPlotBands[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified NumericSplineDef message, length delimited. Does not implicitly {@link epoch_proto.NumericSplineDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.NumericSplineDef
         * @static
         * @param {epoch_proto.INumericSplineDef} message NumericSplineDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericSplineDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NumericSplineDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.NumericSplineDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.NumericSplineDef} NumericSplineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericSplineDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.NumericSplineDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.lines && message.lines.length))
                            message.lines = [];
                        message.lines.push($root.epoch_proto.NumericLine.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        if (!(message.straightLines && message.straightLines.length))
                            message.straightLines = [];
                        message.straightLines.push($root.epoch_proto.StraightLineDef.decode(reader, reader.uint32()));
                        break;
                    }
                case 4: {
                        if (!(message.yPlotBands && message.yPlotBands.length))
                            message.yPlotBands = [];
                        message.yPlotBands.push($root.epoch_proto.Band.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NumericSplineDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.NumericSplineDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.NumericSplineDef} NumericSplineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericSplineDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NumericSplineDef message.
         * @function verify
         * @memberof epoch_proto.NumericSplineDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NumericSplineDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.lines != null && message.hasOwnProperty("lines")) {
                if (!Array.isArray(message.lines))
                    return "lines: array expected";
                for (let i = 0; i < message.lines.length; ++i) {
                    let error = $root.epoch_proto.NumericLine.verify(message.lines[i]);
                    if (error)
                        return "lines." + error;
                }
            }
            if (message.straightLines != null && message.hasOwnProperty("straightLines")) {
                if (!Array.isArray(message.straightLines))
                    return "straightLines: array expected";
                for (let i = 0; i < message.straightLines.length; ++i) {
                    let error = $root.epoch_proto.StraightLineDef.verify(message.straightLines[i]);
                    if (error)
                        return "straightLines." + error;
                }
            }
            if (message.yPlotBands != null && message.hasOwnProperty("yPlotBands")) {
                if (!Array.isArray(message.yPlotBands))
                    return "yPlotBands: array expected";
                for (let i = 0; i < message.yPlotBands.length; ++i) {
                    let error = $root.epoch_proto.Band.verify(message.yPlotBands[i]);
                    if (error)
                        return "yPlotBands." + error;
                }
            }
            return null;
        };

        /**
         * Creates a NumericSplineDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.NumericSplineDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.NumericSplineDef} NumericSplineDef
         */
        NumericSplineDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.NumericSplineDef)
                return object;
            let message = new $root.epoch_proto.NumericSplineDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.NumericSplineDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.lines) {
                if (!Array.isArray(object.lines))
                    throw TypeError(".epoch_proto.NumericSplineDef.lines: array expected");
                message.lines = [];
                for (let i = 0; i < object.lines.length; ++i) {
                    if (typeof object.lines[i] !== "object")
                        throw TypeError(".epoch_proto.NumericSplineDef.lines: object expected");
                    message.lines[i] = $root.epoch_proto.NumericLine.fromObject(object.lines[i]);
                }
            }
            if (object.straightLines) {
                if (!Array.isArray(object.straightLines))
                    throw TypeError(".epoch_proto.NumericSplineDef.straightLines: array expected");
                message.straightLines = [];
                for (let i = 0; i < object.straightLines.length; ++i) {
                    if (typeof object.straightLines[i] !== "object")
                        throw TypeError(".epoch_proto.NumericSplineDef.straightLines: object expected");
                    message.straightLines[i] = $root.epoch_proto.StraightLineDef.fromObject(object.straightLines[i]);
                }
            }
            if (object.yPlotBands) {
                if (!Array.isArray(object.yPlotBands))
                    throw TypeError(".epoch_proto.NumericSplineDef.yPlotBands: array expected");
                message.yPlotBands = [];
                for (let i = 0; i < object.yPlotBands.length; ++i) {
                    if (typeof object.yPlotBands[i] !== "object")
                        throw TypeError(".epoch_proto.NumericSplineDef.yPlotBands: object expected");
                    message.yPlotBands[i] = $root.epoch_proto.Band.fromObject(object.yPlotBands[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a NumericSplineDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.NumericSplineDef
         * @static
         * @param {epoch_proto.NumericSplineDef} message NumericSplineDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NumericSplineDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults) {
                object.lines = [];
                object.straightLines = [];
                object.yPlotBands = [];
            }
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.lines && message.lines.length) {
                object.lines = [];
                for (let j = 0; j < message.lines.length; ++j)
                    object.lines[j] = $root.epoch_proto.NumericLine.toObject(message.lines[j], options);
            }
            if (message.straightLines && message.straightLines.length) {
                object.straightLines = [];
                for (let j = 0; j < message.straightLines.length; ++j)
                    object.straightLines[j] = $root.epoch_proto.StraightLineDef.toObject(message.straightLines[j], options);
            }
            if (message.yPlotBands && message.yPlotBands.length) {
                object.yPlotBands = [];
                for (let j = 0; j < message.yPlotBands.length; ++j)
                    object.yPlotBands[j] = $root.epoch_proto.Band.toObject(message.yPlotBands[j], options);
            }
            return object;
        };

        /**
         * Converts this NumericSplineDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.NumericSplineDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NumericSplineDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NumericSplineDef
         * @function getTypeUrl
         * @memberof epoch_proto.NumericSplineDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NumericSplineDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.NumericSplineDef";
        };

        return NumericSplineDef;
    })();

    epoch_proto.BubblePoint = (function() {

        /**
         * Properties of a BubblePoint.
         * @memberof epoch_proto
         * @interface IBubblePoint
         * @property {number|null} [x] BubblePoint x
         * @property {number|null} [y] BubblePoint y
         * @property {number|null} [z] BubblePoint z
         * @property {string|null} [name] BubblePoint name
         * @property {string|null} [color] BubblePoint color
         */

        /**
         * Constructs a new BubblePoint.
         * @memberof epoch_proto
         * @classdesc Represents a BubblePoint.
         * @implements IBubblePoint
         * @constructor
         * @param {epoch_proto.IBubblePoint=} [properties] Properties to set
         */
        function BubblePoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BubblePoint x.
         * @member {number} x
         * @memberof epoch_proto.BubblePoint
         * @instance
         */
        BubblePoint.prototype.x = 0;

        /**
         * BubblePoint y.
         * @member {number} y
         * @memberof epoch_proto.BubblePoint
         * @instance
         */
        BubblePoint.prototype.y = 0;

        /**
         * BubblePoint z.
         * @member {number} z
         * @memberof epoch_proto.BubblePoint
         * @instance
         */
        BubblePoint.prototype.z = 0;

        /**
         * BubblePoint name.
         * @member {string|null|undefined} name
         * @memberof epoch_proto.BubblePoint
         * @instance
         */
        BubblePoint.prototype.name = null;

        /**
         * BubblePoint color.
         * @member {string|null|undefined} color
         * @memberof epoch_proto.BubblePoint
         * @instance
         */
        BubblePoint.prototype.color = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BubblePoint.prototype, "_name", {
            get: $util.oneOfGetter($oneOfFields = ["name"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BubblePoint.prototype, "_color", {
            get: $util.oneOfGetter($oneOfFields = ["color"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new BubblePoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BubblePoint
         * @static
         * @param {epoch_proto.IBubblePoint=} [properties] Properties to set
         * @returns {epoch_proto.BubblePoint} BubblePoint instance
         */
        BubblePoint.create = function create(properties) {
            return new BubblePoint(properties);
        };

        /**
         * Encodes the specified BubblePoint message. Does not implicitly {@link epoch_proto.BubblePoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BubblePoint
         * @static
         * @param {epoch_proto.IBubblePoint} message BubblePoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BubblePoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 1 =*/9).double(message.x);
            if (message.y != null && Object.hasOwnProperty.call(message, "y"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.y);
            if (message.z != null && Object.hasOwnProperty.call(message, "z"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.z);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.name);
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.color);
            return writer;
        };

        /**
         * Encodes the specified BubblePoint message, length delimited. Does not implicitly {@link epoch_proto.BubblePoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BubblePoint
         * @static
         * @param {epoch_proto.IBubblePoint} message BubblePoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BubblePoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BubblePoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BubblePoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BubblePoint} BubblePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BubblePoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BubblePoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.double();
                        break;
                    }
                case 2: {
                        message.y = reader.double();
                        break;
                    }
                case 3: {
                        message.z = reader.double();
                        break;
                    }
                case 4: {
                        message.name = reader.string();
                        break;
                    }
                case 5: {
                        message.color = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BubblePoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BubblePoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BubblePoint} BubblePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BubblePoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BubblePoint message.
         * @function verify
         * @memberof epoch_proto.BubblePoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BubblePoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x !== "number")
                    return "x: number expected";
            if (message.y != null && message.hasOwnProperty("y"))
                if (typeof message.y !== "number")
                    return "y: number expected";
            if (message.z != null && message.hasOwnProperty("z"))
                if (typeof message.z !== "number")
                    return "z: number expected";
            if (message.name != null && message.hasOwnProperty("name")) {
                properties._name = 1;
                if (!$util.isString(message.name))
                    return "name: string expected";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                properties._color = 1;
                if (!$util.isString(message.color))
                    return "color: string expected";
            }
            return null;
        };

        /**
         * Creates a BubblePoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BubblePoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BubblePoint} BubblePoint
         */
        BubblePoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BubblePoint)
                return object;
            let message = new $root.epoch_proto.BubblePoint();
            if (object.x != null)
                message.x = Number(object.x);
            if (object.y != null)
                message.y = Number(object.y);
            if (object.z != null)
                message.z = Number(object.z);
            if (object.name != null)
                message.name = String(object.name);
            if (object.color != null)
                message.color = String(object.color);
            return message;
        };

        /**
         * Creates a plain object from a BubblePoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BubblePoint
         * @static
         * @param {epoch_proto.BubblePoint} message BubblePoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BubblePoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.x = 0;
                object.y = 0;
                object.z = 0;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                object.x = options.json && !isFinite(message.x) ? String(message.x) : message.x;
            if (message.y != null && message.hasOwnProperty("y"))
                object.y = options.json && !isFinite(message.y) ? String(message.y) : message.y;
            if (message.z != null && message.hasOwnProperty("z"))
                object.z = options.json && !isFinite(message.z) ? String(message.z) : message.z;
            if (message.name != null && message.hasOwnProperty("name")) {
                object.name = message.name;
                if (options.oneofs)
                    object._name = "name";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                object.color = message.color;
                if (options.oneofs)
                    object._color = "color";
            }
            return object;
        };

        /**
         * Converts this BubblePoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.BubblePoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BubblePoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BubblePoint
         * @function getTypeUrl
         * @memberof epoch_proto.BubblePoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BubblePoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BubblePoint";
        };

        return BubblePoint;
    })();

    epoch_proto.BubbleSeries = (function() {

        /**
         * Properties of a BubbleSeries.
         * @memberof epoch_proto
         * @interface IBubbleSeries
         * @property {string|null} [name] BubbleSeries name
         * @property {Array.<epoch_proto.IBubblePoint>|null} [data] BubbleSeries data
         */

        /**
         * Constructs a new BubbleSeries.
         * @memberof epoch_proto
         * @classdesc Represents a BubbleSeries.
         * @implements IBubbleSeries
         * @constructor
         * @param {epoch_proto.IBubbleSeries=} [properties] Properties to set
         */
        function BubbleSeries(properties) {
            this.data = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BubbleSeries name.
         * @member {string} name
         * @memberof epoch_proto.BubbleSeries
         * @instance
         */
        BubbleSeries.prototype.name = "";

        /**
         * BubbleSeries data.
         * @member {Array.<epoch_proto.IBubblePoint>} data
         * @memberof epoch_proto.BubbleSeries
         * @instance
         */
        BubbleSeries.prototype.data = $util.emptyArray;

        /**
         * Creates a new BubbleSeries instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BubbleSeries
         * @static
         * @param {epoch_proto.IBubbleSeries=} [properties] Properties to set
         * @returns {epoch_proto.BubbleSeries} BubbleSeries instance
         */
        BubbleSeries.create = function create(properties) {
            return new BubbleSeries(properties);
        };

        /**
         * Encodes the specified BubbleSeries message. Does not implicitly {@link epoch_proto.BubbleSeries.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BubbleSeries
         * @static
         * @param {epoch_proto.IBubbleSeries} message BubbleSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BubbleSeries.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.name);
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.BubblePoint.encode(message.data[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified BubbleSeries message, length delimited. Does not implicitly {@link epoch_proto.BubbleSeries.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BubbleSeries
         * @static
         * @param {epoch_proto.IBubbleSeries} message BubbleSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BubbleSeries.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BubbleSeries message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BubbleSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BubbleSeries} BubbleSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BubbleSeries.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BubbleSeries();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.name = reader.string();
                        break;
                    }
                case 2: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.BubblePoint.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BubbleSeries message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BubbleSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BubbleSeries} BubbleSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BubbleSeries.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BubbleSeries message.
         * @function verify
         * @memberof epoch_proto.BubbleSeries
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BubbleSeries.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.BubblePoint.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            return null;
        };

        /**
         * Creates a BubbleSeries message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BubbleSeries
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BubbleSeries} BubbleSeries
         */
        BubbleSeries.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BubbleSeries)
                return object;
            let message = new $root.epoch_proto.BubbleSeries();
            if (object.name != null)
                message.name = String(object.name);
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.BubbleSeries.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.BubbleSeries.data: object expected");
                    message.data[i] = $root.epoch_proto.BubblePoint.fromObject(object.data[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a BubbleSeries message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BubbleSeries
         * @static
         * @param {epoch_proto.BubbleSeries} message BubbleSeries
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BubbleSeries.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.data = [];
            if (options.defaults)
                object.name = "";
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.BubblePoint.toObject(message.data[j], options);
            }
            return object;
        };

        /**
         * Converts this BubbleSeries to JSON.
         * @function toJSON
         * @memberof epoch_proto.BubbleSeries
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BubbleSeries.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BubbleSeries
         * @function getTypeUrl
         * @memberof epoch_proto.BubbleSeries
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BubbleSeries.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BubbleSeries";
        };

        return BubbleSeries;
    })();

    epoch_proto.BubbleDef = (function() {

        /**
         * Properties of a BubbleDef.
         * @memberof epoch_proto
         * @interface IBubbleDef
         * @property {epoch_proto.IChartDef|null} [chartDef] BubbleDef chartDef
         * @property {Array.<epoch_proto.IBubbleSeries>|null} [series] BubbleDef series
         * @property {string|null} [minSize] BubbleDef minSize
         * @property {string|null} [maxSize] BubbleDef maxSize
         * @property {string|null} [sizeBy] BubbleDef sizeBy
         */

        /**
         * Constructs a new BubbleDef.
         * @memberof epoch_proto
         * @classdesc Represents a BubbleDef.
         * @implements IBubbleDef
         * @constructor
         * @param {epoch_proto.IBubbleDef=} [properties] Properties to set
         */
        function BubbleDef(properties) {
            this.series = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BubbleDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.BubbleDef
         * @instance
         */
        BubbleDef.prototype.chartDef = null;

        /**
         * BubbleDef series.
         * @member {Array.<epoch_proto.IBubbleSeries>} series
         * @memberof epoch_proto.BubbleDef
         * @instance
         */
        BubbleDef.prototype.series = $util.emptyArray;

        /**
         * BubbleDef minSize.
         * @member {string|null|undefined} minSize
         * @memberof epoch_proto.BubbleDef
         * @instance
         */
        BubbleDef.prototype.minSize = null;

        /**
         * BubbleDef maxSize.
         * @member {string|null|undefined} maxSize
         * @memberof epoch_proto.BubbleDef
         * @instance
         */
        BubbleDef.prototype.maxSize = null;

        /**
         * BubbleDef sizeBy.
         * @member {string|null|undefined} sizeBy
         * @memberof epoch_proto.BubbleDef
         * @instance
         */
        BubbleDef.prototype.sizeBy = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BubbleDef.prototype, "_minSize", {
            get: $util.oneOfGetter($oneOfFields = ["minSize"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BubbleDef.prototype, "_maxSize", {
            get: $util.oneOfGetter($oneOfFields = ["maxSize"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BubbleDef.prototype, "_sizeBy", {
            get: $util.oneOfGetter($oneOfFields = ["sizeBy"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new BubbleDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BubbleDef
         * @static
         * @param {epoch_proto.IBubbleDef=} [properties] Properties to set
         * @returns {epoch_proto.BubbleDef} BubbleDef instance
         */
        BubbleDef.create = function create(properties) {
            return new BubbleDef(properties);
        };

        /**
         * Encodes the specified BubbleDef message. Does not implicitly {@link epoch_proto.BubbleDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BubbleDef
         * @static
         * @param {epoch_proto.IBubbleDef} message BubbleDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BubbleDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.series != null && message.series.length)
                for (let i = 0; i < message.series.length; ++i)
                    $root.epoch_proto.BubbleSeries.encode(message.series[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.minSize != null && Object.hasOwnProperty.call(message, "minSize"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.minSize);
            if (message.maxSize != null && Object.hasOwnProperty.call(message, "maxSize"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.maxSize);
            if (message.sizeBy != null && Object.hasOwnProperty.call(message, "sizeBy"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.sizeBy);
            return writer;
        };

        /**
         * Encodes the specified BubbleDef message, length delimited. Does not implicitly {@link epoch_proto.BubbleDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BubbleDef
         * @static
         * @param {epoch_proto.IBubbleDef} message BubbleDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BubbleDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BubbleDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BubbleDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BubbleDef} BubbleDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BubbleDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BubbleDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.series && message.series.length))
                            message.series = [];
                        message.series.push($root.epoch_proto.BubbleSeries.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.minSize = reader.string();
                        break;
                    }
                case 4: {
                        message.maxSize = reader.string();
                        break;
                    }
                case 5: {
                        message.sizeBy = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BubbleDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BubbleDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BubbleDef} BubbleDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BubbleDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BubbleDef message.
         * @function verify
         * @memberof epoch_proto.BubbleDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BubbleDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.series != null && message.hasOwnProperty("series")) {
                if (!Array.isArray(message.series))
                    return "series: array expected";
                for (let i = 0; i < message.series.length; ++i) {
                    let error = $root.epoch_proto.BubbleSeries.verify(message.series[i]);
                    if (error)
                        return "series." + error;
                }
            }
            if (message.minSize != null && message.hasOwnProperty("minSize")) {
                properties._minSize = 1;
                if (!$util.isString(message.minSize))
                    return "minSize: string expected";
            }
            if (message.maxSize != null && message.hasOwnProperty("maxSize")) {
                properties._maxSize = 1;
                if (!$util.isString(message.maxSize))
                    return "maxSize: string expected";
            }
            if (message.sizeBy != null && message.hasOwnProperty("sizeBy")) {
                properties._sizeBy = 1;
                if (!$util.isString(message.sizeBy))
                    return "sizeBy: string expected";
            }
            return null;
        };

        /**
         * Creates a BubbleDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BubbleDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BubbleDef} BubbleDef
         */
        BubbleDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BubbleDef)
                return object;
            let message = new $root.epoch_proto.BubbleDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.BubbleDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.series) {
                if (!Array.isArray(object.series))
                    throw TypeError(".epoch_proto.BubbleDef.series: array expected");
                message.series = [];
                for (let i = 0; i < object.series.length; ++i) {
                    if (typeof object.series[i] !== "object")
                        throw TypeError(".epoch_proto.BubbleDef.series: object expected");
                    message.series[i] = $root.epoch_proto.BubbleSeries.fromObject(object.series[i]);
                }
            }
            if (object.minSize != null)
                message.minSize = String(object.minSize);
            if (object.maxSize != null)
                message.maxSize = String(object.maxSize);
            if (object.sizeBy != null)
                message.sizeBy = String(object.sizeBy);
            return message;
        };

        /**
         * Creates a plain object from a BubbleDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BubbleDef
         * @static
         * @param {epoch_proto.BubbleDef} message BubbleDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BubbleDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.series = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.series && message.series.length) {
                object.series = [];
                for (let j = 0; j < message.series.length; ++j)
                    object.series[j] = $root.epoch_proto.BubbleSeries.toObject(message.series[j], options);
            }
            if (message.minSize != null && message.hasOwnProperty("minSize")) {
                object.minSize = message.minSize;
                if (options.oneofs)
                    object._minSize = "minSize";
            }
            if (message.maxSize != null && message.hasOwnProperty("maxSize")) {
                object.maxSize = message.maxSize;
                if (options.oneofs)
                    object._maxSize = "maxSize";
            }
            if (message.sizeBy != null && message.hasOwnProperty("sizeBy")) {
                object.sizeBy = message.sizeBy;
                if (options.oneofs)
                    object._sizeBy = "sizeBy";
            }
            return object;
        };

        /**
         * Converts this BubbleDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.BubbleDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BubbleDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BubbleDef
         * @function getTypeUrl
         * @memberof epoch_proto.BubbleDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BubbleDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BubbleDef";
        };

        return BubbleDef;
    })();

    epoch_proto.TreemapPoint = (function() {

        /**
         * Properties of a TreemapPoint.
         * @memberof epoch_proto
         * @interface ITreemapPoint
         * @property {string|null} [id] TreemapPoint id
         * @property {string|null} [parent] TreemapPoint parent
         * @property {string|null} [name] TreemapPoint name
         * @property {number|null} [value] TreemapPoint value
         * @property {string|null} [color] TreemapPoint color
         * @property {number|null} [colorValue] TreemapPoint colorValue
         */

        /**
         * Constructs a new TreemapPoint.
         * @memberof epoch_proto
         * @classdesc Represents a TreemapPoint.
         * @implements ITreemapPoint
         * @constructor
         * @param {epoch_proto.ITreemapPoint=} [properties] Properties to set
         */
        function TreemapPoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * TreemapPoint id.
         * @member {string} id
         * @memberof epoch_proto.TreemapPoint
         * @instance
         */
        TreemapPoint.prototype.id = "";

        /**
         * TreemapPoint parent.
         * @member {string|null|undefined} parent
         * @memberof epoch_proto.TreemapPoint
         * @instance
         */
        TreemapPoint.prototype.parent = null;

        /**
         * TreemapPoint name.
         * @member {string} name
         * @memberof epoch_proto.TreemapPoint
         * @instance
         */
        TreemapPoint.prototype.name = "";

        /**
         * TreemapPoint value.
         * @member {number|null|undefined} value
         * @memberof epoch_proto.TreemapPoint
         * @instance
         */
        TreemapPoint.prototype.value = null;

        /**
         * TreemapPoint color.
         * @member {string|null|undefined} color
         * @memberof epoch_proto.TreemapPoint
         * @instance
         */
        TreemapPoint.prototype.color = null;

        /**
         * TreemapPoint colorValue.
         * @member {number|null|undefined} colorValue
         * @memberof epoch_proto.TreemapPoint
         * @instance
         */
        TreemapPoint.prototype.colorValue = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(TreemapPoint.prototype, "_parent", {
            get: $util.oneOfGetter($oneOfFields = ["parent"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(TreemapPoint.prototype, "_value", {
            get: $util.oneOfGetter($oneOfFields = ["value"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(TreemapPoint.prototype, "_color", {
            get: $util.oneOfGetter($oneOfFields = ["color"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(TreemapPoint.prototype, "_colorValue", {
            get: $util.oneOfGetter($oneOfFields = ["colorValue"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new TreemapPoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.TreemapPoint
         * @static
         * @param {epoch_proto.ITreemapPoint=} [properties] Properties to set
         * @returns {epoch_proto.TreemapPoint} TreemapPoint instance
         */
        TreemapPoint.create = function create(properties) {
            return new TreemapPoint(properties);
        };

        /**
         * Encodes the specified TreemapPoint message. Does not implicitly {@link epoch_proto.TreemapPoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.TreemapPoint
         * @static
         * @param {epoch_proto.ITreemapPoint} message TreemapPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TreemapPoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.parent != null && Object.hasOwnProperty.call(message, "parent"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.parent);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.name);
            if (message.value != null && Object.hasOwnProperty.call(message, "value"))
                writer.uint32(/* id 4, wireType 1 =*/33).double(message.value);
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.color);
            if (message.colorValue != null && Object.hasOwnProperty.call(message, "colorValue"))
                writer.uint32(/* id 6, wireType 1 =*/49).double(message.colorValue);
            return writer;
        };

        /**
         * Encodes the specified TreemapPoint message, length delimited. Does not implicitly {@link epoch_proto.TreemapPoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.TreemapPoint
         * @static
         * @param {epoch_proto.ITreemapPoint} message TreemapPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TreemapPoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a TreemapPoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.TreemapPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.TreemapPoint} TreemapPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TreemapPoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.TreemapPoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.parent = reader.string();
                        break;
                    }
                case 3: {
                        message.name = reader.string();
                        break;
                    }
                case 4: {
                        message.value = reader.double();
                        break;
                    }
                case 5: {
                        message.color = reader.string();
                        break;
                    }
                case 6: {
                        message.colorValue = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a TreemapPoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.TreemapPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.TreemapPoint} TreemapPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TreemapPoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a TreemapPoint message.
         * @function verify
         * @memberof epoch_proto.TreemapPoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        TreemapPoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.parent != null && message.hasOwnProperty("parent")) {
                properties._parent = 1;
                if (!$util.isString(message.parent))
                    return "parent: string expected";
            }
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.value != null && message.hasOwnProperty("value")) {
                properties._value = 1;
                if (typeof message.value !== "number")
                    return "value: number expected";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                properties._color = 1;
                if (!$util.isString(message.color))
                    return "color: string expected";
            }
            if (message.colorValue != null && message.hasOwnProperty("colorValue")) {
                properties._colorValue = 1;
                if (typeof message.colorValue !== "number")
                    return "colorValue: number expected";
            }
            return null;
        };

        /**
         * Creates a TreemapPoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.TreemapPoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.TreemapPoint} TreemapPoint
         */
        TreemapPoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.TreemapPoint)
                return object;
            let message = new $root.epoch_proto.TreemapPoint();
            if (object.id != null)
                message.id = String(object.id);
            if (object.parent != null)
                message.parent = String(object.parent);
            if (object.name != null)
                message.name = String(object.name);
            if (object.value != null)
                message.value = Number(object.value);
            if (object.color != null)
                message.color = String(object.color);
            if (object.colorValue != null)
                message.colorValue = Number(object.colorValue);
            return message;
        };

        /**
         * Creates a plain object from a TreemapPoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.TreemapPoint
         * @static
         * @param {epoch_proto.TreemapPoint} message TreemapPoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        TreemapPoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.id = "";
                object.name = "";
            }
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.parent != null && message.hasOwnProperty("parent")) {
                object.parent = message.parent;
                if (options.oneofs)
                    object._parent = "parent";
            }
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.value != null && message.hasOwnProperty("value")) {
                object.value = options.json && !isFinite(message.value) ? String(message.value) : message.value;
                if (options.oneofs)
                    object._value = "value";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                object.color = message.color;
                if (options.oneofs)
                    object._color = "color";
            }
            if (message.colorValue != null && message.hasOwnProperty("colorValue")) {
                object.colorValue = options.json && !isFinite(message.colorValue) ? String(message.colorValue) : message.colorValue;
                if (options.oneofs)
                    object._colorValue = "colorValue";
            }
            return object;
        };

        /**
         * Converts this TreemapPoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.TreemapPoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        TreemapPoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for TreemapPoint
         * @function getTypeUrl
         * @memberof epoch_proto.TreemapPoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        TreemapPoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.TreemapPoint";
        };

        return TreemapPoint;
    })();

    epoch_proto.TreemapDef = (function() {

        /**
         * Properties of a TreemapDef.
         * @memberof epoch_proto
         * @interface ITreemapDef
         * @property {epoch_proto.IChartDef|null} [chartDef] TreemapDef chartDef
         * @property {Array.<epoch_proto.ITreemapPoint>|null} [points] TreemapDef points
         * @property {string|null} [layoutAlgorithm] TreemapDef layoutAlgorithm
         */

        /**
         * Constructs a new TreemapDef.
         * @memberof epoch_proto
         * @classdesc Represents a TreemapDef.
         * @implements ITreemapDef
         * @constructor
         * @param {epoch_proto.ITreemapDef=} [properties] Properties to set
         */
        function TreemapDef(properties) {
            this.points = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * TreemapDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.TreemapDef
         * @instance
         */
        TreemapDef.prototype.chartDef = null;

        /**
         * TreemapDef points.
         * @member {Array.<epoch_proto.ITreemapPoint>} points
         * @memberof epoch_proto.TreemapDef
         * @instance
         */
        TreemapDef.prototype.points = $util.emptyArray;

        /**
         * TreemapDef layoutAlgorithm.
         * @member {string|null|undefined} layoutAlgorithm
         * @memberof epoch_proto.TreemapDef
         * @instance
         */
        TreemapDef.prototype.layoutAlgorithm = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(TreemapDef.prototype, "_layoutAlgorithm", {
            get: $util.oneOfGetter($oneOfFields = ["layoutAlgorithm"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new TreemapDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.TreemapDef
         * @static
         * @param {epoch_proto.ITreemapDef=} [properties] Properties to set
         * @returns {epoch_proto.TreemapDef} TreemapDef instance
         */
        TreemapDef.create = function create(properties) {
            return new TreemapDef(properties);
        };

        /**
         * Encodes the specified TreemapDef message. Does not implicitly {@link epoch_proto.TreemapDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.TreemapDef
         * @static
         * @param {epoch_proto.ITreemapDef} message TreemapDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TreemapDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.points != null && message.points.length)
                for (let i = 0; i < message.points.length; ++i)
                    $root.epoch_proto.TreemapPoint.encode(message.points[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.layoutAlgorithm != null && Object.hasOwnProperty.call(message, "layoutAlgorithm"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.layoutAlgorithm);
            return writer;
        };

        /**
         * Encodes the specified TreemapDef message, length delimited. Does not implicitly {@link epoch_proto.TreemapDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.TreemapDef
         * @static
         * @param {epoch_proto.ITreemapDef} message TreemapDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TreemapDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a TreemapDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.TreemapDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.TreemapDef} TreemapDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TreemapDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.TreemapDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.points && message.points.length))
                            message.points = [];
                        message.points.push($root.epoch_proto.TreemapPoint.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.layoutAlgorithm = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a TreemapDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.TreemapDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.TreemapDef} TreemapDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TreemapDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a TreemapDef message.
         * @function verify
         * @memberof epoch_proto.TreemapDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        TreemapDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.points != null && message.hasOwnProperty("points")) {
                if (!Array.isArray(message.points))
                    return "points: array expected";
                for (let i = 0; i < message.points.length; ++i) {
                    let error = $root.epoch_proto.TreemapPoint.verify(message.points[i]);
                    if (error)
                        return "points." + error;
                }
            }
            if (message.layoutAlgorithm != null && message.hasOwnProperty("layoutAlgorithm")) {
                properties._layoutAlgorithm = 1;
                if (!$util.isString(message.layoutAlgorithm))
                    return "layoutAlgorithm: string expected";
            }
            return null;
        };

        /**
         * Creates a TreemapDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.TreemapDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.TreemapDef} TreemapDef
         */
        TreemapDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.TreemapDef)
                return object;
            let message = new $root.epoch_proto.TreemapDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.TreemapDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.points) {
                if (!Array.isArray(object.points))
                    throw TypeError(".epoch_proto.TreemapDef.points: array expected");
                message.points = [];
                for (let i = 0; i < object.points.length; ++i) {
                    if (typeof object.points[i] !== "object")
                        throw TypeError(".epoch_proto.TreemapDef.points: object expected");
                    message.points[i] = $root.epoch_proto.TreemapPoint.fromObject(object.points[i]);
                }
            }
            if (object.layoutAlgorithm != null)
                message.layoutAlgorithm = String(object.layoutAlgorithm);
            return message;
        };

        /**
         * Creates a plain object from a TreemapDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.TreemapDef
         * @static
         * @param {epoch_proto.TreemapDef} message TreemapDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        TreemapDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.points = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.points && message.points.length) {
                object.points = [];
                for (let j = 0; j < message.points.length; ++j)
                    object.points[j] = $root.epoch_proto.TreemapPoint.toObject(message.points[j], options);
            }
            if (message.layoutAlgorithm != null && message.hasOwnProperty("layoutAlgorithm")) {
                object.layoutAlgorithm = message.layoutAlgorithm;
                if (options.oneofs)
                    object._layoutAlgorithm = "layoutAlgorithm";
            }
            return object;
        };

        /**
         * Converts this TreemapDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.TreemapDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        TreemapDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for TreemapDef
         * @function getTypeUrl
         * @memberof epoch_proto.TreemapDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        TreemapDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.TreemapDef";
        };

        return TreemapDef;
    })();

    epoch_proto.SankeyLink = (function() {

        /**
         * Properties of a SankeyLink.
         * @memberof epoch_proto
         * @interface ISankeyLink
         * @property {string|null} [from] SankeyLink from
         * @property {string|null} [to] SankeyLink to
         * @property {number|null} [weight] SankeyLink weight
         * @property {string|null} [color] SankeyLink color
         */

        /**
         * Constructs a new SankeyLink.
         * @memberof epoch_proto
         * @classdesc Represents a SankeyLink.
         * @implements ISankeyLink
         * @constructor
         * @param {epoch_proto.ISankeyLink=} [properties] Properties to set
         */
        function SankeyLink(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * SankeyLink from.
         * @member {string} from
         * @memberof epoch_proto.SankeyLink
         * @instance
         */
        SankeyLink.prototype.from = "";

        /**
         * SankeyLink to.
         * @member {string} to
         * @memberof epoch_proto.SankeyLink
         * @instance
         */
        SankeyLink.prototype.to = "";

        /**
         * SankeyLink weight.
         * @member {number} weight
         * @memberof epoch_proto.SankeyLink
         * @instance
         */
        SankeyLink.prototype.weight = 0;

        /**
         * SankeyLink color.
         * @member {string|null|undefined} color
         * @memberof epoch_proto.SankeyLink
         * @instance
         */
        SankeyLink.prototype.color = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(SankeyLink.prototype, "_color", {
            get: $util.oneOfGetter($oneOfFields = ["color"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new SankeyLink instance using the specified properties.
         * @function create
         * @memberof epoch_proto.SankeyLink
         * @static
         * @param {epoch_proto.ISankeyLink=} [properties] Properties to set
         * @returns {epoch_proto.SankeyLink} SankeyLink instance
         */
        SankeyLink.create = function create(properties) {
            return new SankeyLink(properties);
        };

        /**
         * Encodes the specified SankeyLink message. Does not implicitly {@link epoch_proto.SankeyLink.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.SankeyLink
         * @static
         * @param {epoch_proto.ISankeyLink} message SankeyLink message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SankeyLink.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.from != null && Object.hasOwnProperty.call(message, "from"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.from);
            if (message.to != null && Object.hasOwnProperty.call(message, "to"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.to);
            if (message.weight != null && Object.hasOwnProperty.call(message, "weight"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.weight);
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.color);
            return writer;
        };

        /**
         * Encodes the specified SankeyLink message, length delimited. Does not implicitly {@link epoch_proto.SankeyLink.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.SankeyLink
         * @static
         * @param {epoch_proto.ISankeyLink} message SankeyLink message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SankeyLink.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a SankeyLink message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.SankeyLink
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.SankeyLink} SankeyLink
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SankeyLink.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.SankeyLink();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.from = reader.string();
                        break;
                    }
                case 2: {
                        message.to = reader.string();
                        break;
                    }
                case 3: {
                        message.weight = reader.double();
                        break;
                    }
                case 4: {
                        message.color = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a SankeyLink message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.SankeyLink
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.SankeyLink} SankeyLink
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SankeyLink.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a SankeyLink message.
         * @function verify
         * @memberof epoch_proto.SankeyLink
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        SankeyLink.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.from != null && message.hasOwnProperty("from"))
                if (!$util.isString(message.from))
                    return "from: string expected";
            if (message.to != null && message.hasOwnProperty("to"))
                if (!$util.isString(message.to))
                    return "to: string expected";
            if (message.weight != null && message.hasOwnProperty("weight"))
                if (typeof message.weight !== "number")
                    return "weight: number expected";
            if (message.color != null && message.hasOwnProperty("color")) {
                properties._color = 1;
                if (!$util.isString(message.color))
                    return "color: string expected";
            }
            return null;
        };

        /**
         * Creates a SankeyLink message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.SankeyLink
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.SankeyLink} SankeyLink
         */
        SankeyLink.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.SankeyLink)
                return object;
            let message = new $root.epoch_proto.SankeyLink();
            if (object.from != null)
                message.from = String(object.from);
            if (object.to != null)
                message.to = String(object.to);
            if (object.weight != null)
                message.weight = Number(object.weight);
            if (object.color != null)
                message.color = String(object.color);
            return message;
        };

        /**
         * Creates a plain object from a SankeyLink message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.SankeyLink
         * @static
         * @param {epoch_proto.SankeyLink} message SankeyLink
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        SankeyLink.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.from = "";
                object.to = "";
                object.weight = 0;
            }
            if (message.from != null && message.hasOwnProperty("from"))
                object.from = message.from;
            if (message.to != null && message.hasOwnProperty("to"))
                object.to = message.to;
            if (message.weight != null && message.hasOwnProperty("weight"))
                object.weight = options.json && !isFinite(message.weight) ? String(message.weight) : message.weight;
            if (message.color != null && message.hasOwnProperty("color")) {
                object.color = message.color;
                if (options.oneofs)
                    object._color = "color";
            }
            return object;
        };

        /**
         * Converts this SankeyLink to JSON.
         * @function toJSON
         * @memberof epoch_proto.SankeyLink
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        SankeyLink.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for SankeyLink
         * @function getTypeUrl
         * @memberof epoch_proto.SankeyLink
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        SankeyLink.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.SankeyLink";
        };

        return SankeyLink;
    })();

    epoch_proto.SankeyNode = (function() {

        /**
         * Properties of a SankeyNode.
         * @memberof epoch_proto
         * @interface ISankeyNode
         * @property {string|null} [id] SankeyNode id
         * @property {string|null} [name] SankeyNode name
         * @property {string|null} [color] SankeyNode color
         */

        /**
         * Constructs a new SankeyNode.
         * @memberof epoch_proto
         * @classdesc Represents a SankeyNode.
         * @implements ISankeyNode
         * @constructor
         * @param {epoch_proto.ISankeyNode=} [properties] Properties to set
         */
        function SankeyNode(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * SankeyNode id.
         * @member {string} id
         * @memberof epoch_proto.SankeyNode
         * @instance
         */
        SankeyNode.prototype.id = "";

        /**
         * SankeyNode name.
         * @member {string|null|undefined} name
         * @memberof epoch_proto.SankeyNode
         * @instance
         */
        SankeyNode.prototype.name = null;

        /**
         * SankeyNode color.
         * @member {string|null|undefined} color
         * @memberof epoch_proto.SankeyNode
         * @instance
         */
        SankeyNode.prototype.color = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(SankeyNode.prototype, "_name", {
            get: $util.oneOfGetter($oneOfFields = ["name"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(SankeyNode.prototype, "_color", {
            get: $util.oneOfGetter($oneOfFields = ["color"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new SankeyNode instance using the specified properties.
         * @function create
         * @memberof epoch_proto.SankeyNode
         * @static
         * @param {epoch_proto.ISankeyNode=} [properties] Properties to set
         * @returns {epoch_proto.SankeyNode} SankeyNode instance
         */
        SankeyNode.create = function create(properties) {
            return new SankeyNode(properties);
        };

        /**
         * Encodes the specified SankeyNode message. Does not implicitly {@link epoch_proto.SankeyNode.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.SankeyNode
         * @static
         * @param {epoch_proto.ISankeyNode} message SankeyNode message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SankeyNode.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.id != null && Object.hasOwnProperty.call(message, "id"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.id);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.name);
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.color);
            return writer;
        };

        /**
         * Encodes the specified SankeyNode message, length delimited. Does not implicitly {@link epoch_proto.SankeyNode.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.SankeyNode
         * @static
         * @param {epoch_proto.ISankeyNode} message SankeyNode message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SankeyNode.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a SankeyNode message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.SankeyNode
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.SankeyNode} SankeyNode
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SankeyNode.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.SankeyNode();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.id = reader.string();
                        break;
                    }
                case 2: {
                        message.name = reader.string();
                        break;
                    }
                case 3: {
                        message.color = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a SankeyNode message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.SankeyNode
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.SankeyNode} SankeyNode
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SankeyNode.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a SankeyNode message.
         * @function verify
         * @memberof epoch_proto.SankeyNode
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        SankeyNode.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.id != null && message.hasOwnProperty("id"))
                if (!$util.isString(message.id))
                    return "id: string expected";
            if (message.name != null && message.hasOwnProperty("name")) {
                properties._name = 1;
                if (!$util.isString(message.name))
                    return "name: string expected";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                properties._color = 1;
                if (!$util.isString(message.color))
                    return "color: string expected";
            }
            return null;
        };

        /**
         * Creates a SankeyNode message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.SankeyNode
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.SankeyNode} SankeyNode
         */
        SankeyNode.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.SankeyNode)
                return object;
            let message = new $root.epoch_proto.SankeyNode();
            if (object.id != null)
                message.id = String(object.id);
            if (object.name != null)
                message.name = String(object.name);
            if (object.color != null)
                message.color = String(object.color);
            return message;
        };

        /**
         * Creates a plain object from a SankeyNode message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.SankeyNode
         * @static
         * @param {epoch_proto.SankeyNode} message SankeyNode
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        SankeyNode.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults)
                object.id = "";
            if (message.id != null && message.hasOwnProperty("id"))
                object.id = message.id;
            if (message.name != null && message.hasOwnProperty("name")) {
                object.name = message.name;
                if (options.oneofs)
                    object._name = "name";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                object.color = message.color;
                if (options.oneofs)
                    object._color = "color";
            }
            return object;
        };

        /**
         * Converts this SankeyNode to JSON.
         * @function toJSON
         * @memberof epoch_proto.SankeyNode
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        SankeyNode.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for SankeyNode
         * @function getTypeUrl
         * @memberof epoch_proto.SankeyNode
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        SankeyNode.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.SankeyNode";
        };

        return SankeyNode;
    })();

    epoch_proto.SankeyDef = (function() {

        /**
         * Properties of a SankeyDef.
         * @memberof epoch_proto
         * @interface ISankeyDef
         * @property {epoch_proto.IChartDef|null} [chartDef] SankeyDef chartDef
         * @property {Array.<epoch_proto.ISankeyLink>|null} [links] SankeyDef links
         * @property {Array.<epoch_proto.ISankeyNode>|null} [nodes] SankeyDef nodes
         * @property {number|null} [curveFactor] SankeyDef curveFactor
         */

        /**
         * Constructs a new SankeyDef.
         * @memberof epoch_proto
         * @classdesc Represents a SankeyDef.
         * @implements ISankeyDef
         * @constructor
         * @param {epoch_proto.ISankeyDef=} [properties] Properties to set
         */
        function SankeyDef(properties) {
            this.links = [];
            this.nodes = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * SankeyDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.SankeyDef
         * @instance
         */
        SankeyDef.prototype.chartDef = null;

        /**
         * SankeyDef links.
         * @member {Array.<epoch_proto.ISankeyLink>} links
         * @memberof epoch_proto.SankeyDef
         * @instance
         */
        SankeyDef.prototype.links = $util.emptyArray;

        /**
         * SankeyDef nodes.
         * @member {Array.<epoch_proto.ISankeyNode>} nodes
         * @memberof epoch_proto.SankeyDef
         * @instance
         */
        SankeyDef.prototype.nodes = $util.emptyArray;

        /**
         * SankeyDef curveFactor.
         * @member {number|null|undefined} curveFactor
         * @memberof epoch_proto.SankeyDef
         * @instance
         */
        SankeyDef.prototype.curveFactor = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(SankeyDef.prototype, "_curveFactor", {
            get: $util.oneOfGetter($oneOfFields = ["curveFactor"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new SankeyDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.SankeyDef
         * @static
         * @param {epoch_proto.ISankeyDef=} [properties] Properties to set
         * @returns {epoch_proto.SankeyDef} SankeyDef instance
         */
        SankeyDef.create = function create(properties) {
            return new SankeyDef(properties);
        };

        /**
         * Encodes the specified SankeyDef message. Does not implicitly {@link epoch_proto.SankeyDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.SankeyDef
         * @static
         * @param {epoch_proto.ISankeyDef} message SankeyDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SankeyDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.links != null && message.links.length)
                for (let i = 0; i < message.links.length; ++i)
                    $root.epoch_proto.SankeyLink.encode(message.links[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.nodes != null && message.nodes.length)
                for (let i = 0; i < message.nodes.length; ++i)
                    $root.epoch_proto.SankeyNode.encode(message.nodes[i], writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.curveFactor != null && Object.hasOwnProperty.call(message, "curveFactor"))
                writer.uint32(/* id 4, wireType 1 =*/33).double(message.curveFactor);
            return writer;
        };

        /**
         * Encodes the specified SankeyDef message, length delimited. Does not implicitly {@link epoch_proto.SankeyDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.SankeyDef
         * @static
         * @param {epoch_proto.ISankeyDef} message SankeyDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        SankeyDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a SankeyDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.SankeyDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.SankeyDef} SankeyDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SankeyDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.SankeyDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.links && message.links.length))
                            message.links = [];
                        message.links.push($root.epoch_proto.SankeyLink.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        if (!(message.nodes && message.nodes.length))
                            message.nodes = [];
                        message.nodes.push($root.epoch_proto.SankeyNode.decode(reader, reader.uint32()));
                        break;
                    }
                case 4: {
                        message.curveFactor = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a SankeyDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.SankeyDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.SankeyDef} SankeyDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        SankeyDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a SankeyDef message.
         * @function verify
         * @memberof epoch_proto.SankeyDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        SankeyDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.links != null && message.hasOwnProperty("links")) {
                if (!Array.isArray(message.links))
                    return "links: array expected";
                for (let i = 0; i < message.links.length; ++i) {
                    let error = $root.epoch_proto.SankeyLink.verify(message.links[i]);
                    if (error)
                        return "links." + error;
                }
            }
            if (message.nodes != null && message.hasOwnProperty("nodes")) {
                if (!Array.isArray(message.nodes))
                    return "nodes: array expected";
                for (let i = 0; i < message.nodes.length; ++i) {
                    let error = $root.epoch_proto.SankeyNode.verify(message.nodes[i]);
                    if (error)
                        return "nodes." + error;
                }
            }
            if (message.curveFactor != null && message.hasOwnProperty("curveFactor")) {
                properties._curveFactor = 1;
                if (typeof message.curveFactor !== "number")
                    return "curveFactor: number expected";
            }
            return null;
        };

        /**
         * Creates a SankeyDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.SankeyDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.SankeyDef} SankeyDef
         */
        SankeyDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.SankeyDef)
                return object;
            let message = new $root.epoch_proto.SankeyDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.SankeyDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.links) {
                if (!Array.isArray(object.links))
                    throw TypeError(".epoch_proto.SankeyDef.links: array expected");
                message.links = [];
                for (let i = 0; i < object.links.length; ++i) {
                    if (typeof object.links[i] !== "object")
                        throw TypeError(".epoch_proto.SankeyDef.links: object expected");
                    message.links[i] = $root.epoch_proto.SankeyLink.fromObject(object.links[i]);
                }
            }
            if (object.nodes) {
                if (!Array.isArray(object.nodes))
                    throw TypeError(".epoch_proto.SankeyDef.nodes: array expected");
                message.nodes = [];
                for (let i = 0; i < object.nodes.length; ++i) {
                    if (typeof object.nodes[i] !== "object")
                        throw TypeError(".epoch_proto.SankeyDef.nodes: object expected");
                    message.nodes[i] = $root.epoch_proto.SankeyNode.fromObject(object.nodes[i]);
                }
            }
            if (object.curveFactor != null)
                message.curveFactor = Number(object.curveFactor);
            return message;
        };

        /**
         * Creates a plain object from a SankeyDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.SankeyDef
         * @static
         * @param {epoch_proto.SankeyDef} message SankeyDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        SankeyDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults) {
                object.links = [];
                object.nodes = [];
            }
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.links && message.links.length) {
                object.links = [];
                for (let j = 0; j < message.links.length; ++j)
                    object.links[j] = $root.epoch_proto.SankeyLink.toObject(message.links[j], options);
            }
            if (message.nodes && message.nodes.length) {
                object.nodes = [];
                for (let j = 0; j < message.nodes.length; ++j)
                    object.nodes[j] = $root.epoch_proto.SankeyNode.toObject(message.nodes[j], options);
            }
            if (message.curveFactor != null && message.hasOwnProperty("curveFactor")) {
                object.curveFactor = options.json && !isFinite(message.curveFactor) ? String(message.curveFactor) : message.curveFactor;
                if (options.oneofs)
                    object._curveFactor = "curveFactor";
            }
            return object;
        };

        /**
         * Converts this SankeyDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.SankeyDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        SankeyDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for SankeyDef
         * @function getTypeUrl
         * @memberof epoch_proto.SankeyDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        SankeyDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.SankeyDef";
        };

        return SankeyDef;
    })();

    epoch_proto.AreaRangePoint = (function() {

        /**
         * Properties of an AreaRangePoint.
         * @memberof epoch_proto
         * @interface IAreaRangePoint
         * @property {number|Long|null} [x] AreaRangePoint x
         * @property {number|null} [low] AreaRangePoint low
         * @property {number|null} [high] AreaRangePoint high
         */

        /**
         * Constructs a new AreaRangePoint.
         * @memberof epoch_proto
         * @classdesc Represents an AreaRangePoint.
         * @implements IAreaRangePoint
         * @constructor
         * @param {epoch_proto.IAreaRangePoint=} [properties] Properties to set
         */
        function AreaRangePoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * AreaRangePoint x.
         * @member {number|Long} x
         * @memberof epoch_proto.AreaRangePoint
         * @instance
         */
        AreaRangePoint.prototype.x = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * AreaRangePoint low.
         * @member {number} low
         * @memberof epoch_proto.AreaRangePoint
         * @instance
         */
        AreaRangePoint.prototype.low = 0;

        /**
         * AreaRangePoint high.
         * @member {number} high
         * @memberof epoch_proto.AreaRangePoint
         * @instance
         */
        AreaRangePoint.prototype.high = 0;

        /**
         * Creates a new AreaRangePoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.AreaRangePoint
         * @static
         * @param {epoch_proto.IAreaRangePoint=} [properties] Properties to set
         * @returns {epoch_proto.AreaRangePoint} AreaRangePoint instance
         */
        AreaRangePoint.create = function create(properties) {
            return new AreaRangePoint(properties);
        };

        /**
         * Encodes the specified AreaRangePoint message. Does not implicitly {@link epoch_proto.AreaRangePoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.AreaRangePoint
         * @static
         * @param {epoch_proto.IAreaRangePoint} message AreaRangePoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AreaRangePoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 0 =*/8).int64(message.x);
            if (message.low != null && Object.hasOwnProperty.call(message, "low"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.low);
            if (message.high != null && Object.hasOwnProperty.call(message, "high"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.high);
            return writer;
        };

        /**
         * Encodes the specified AreaRangePoint message, length delimited. Does not implicitly {@link epoch_proto.AreaRangePoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.AreaRangePoint
         * @static
         * @param {epoch_proto.IAreaRangePoint} message AreaRangePoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AreaRangePoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an AreaRangePoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.AreaRangePoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.AreaRangePoint} AreaRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AreaRangePoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.AreaRangePoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.int64();
                        break;
                    }
                case 2: {
                        message.low = reader.double();
                        break;
                    }
                case 3: {
                        message.high = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an AreaRangePoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.AreaRangePoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.AreaRangePoint} AreaRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AreaRangePoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an AreaRangePoint message.
         * @function verify
         * @memberof epoch_proto.AreaRangePoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        AreaRangePoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.x != null && message.hasOwnProperty("x"))
                if (!$util.isInteger(message.x) && !(message.x && $util.isInteger(message.x.low) && $util.isInteger(message.x.high)))
                    return "x: integer|Long expected";
            if (message.low != null && message.hasOwnProperty("low"))
                if (typeof message.low !== "number")
                    return "low: number expected";
            if (message.high != null && message.hasOwnProperty("high"))
                if (typeof message.high !== "number")
                    return "high: number expected";
            return null;
        };

        /**
         * Creates an AreaRangePoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.AreaRangePoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.AreaRangePoint} AreaRangePoint
         */
        AreaRangePoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.AreaRangePoint)
                return object;
            let message = new $root.epoch_proto.AreaRangePoint();
            if (object.x != null)
                if ($util.Long)
                    (message.x = $util.Long.fromValue(object.x)).unsigned = false;
                else if (typeof object.x === "string")
                    message.x = parseInt(object.x, 10);
                else if (typeof object.x === "number")
                    message.x = object.x;
                else if (typeof object.x === "object")
                    message.x = new $util.LongBits(object.x.low >>> 0, object.x.high >>> 0).toNumber();
            if (object.low != null)
                message.low = Number(object.low);
            if (object.high != null)
                message.high = Number(object.high);
            return message;
        };

        /**
         * Creates a plain object from an AreaRangePoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.AreaRangePoint
         * @static
         * @param {epoch_proto.AreaRangePoint} message AreaRangePoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        AreaRangePoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                if ($util.Long) {
                    let long = new $util.Long(0, 0, false);
                    object.x = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.x = options.longs === String ? "0" : 0;
                object.low = 0;
                object.high = 0;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x === "number")
                    object.x = options.longs === String ? String(message.x) : message.x;
                else
                    object.x = options.longs === String ? $util.Long.prototype.toString.call(message.x) : options.longs === Number ? new $util.LongBits(message.x.low >>> 0, message.x.high >>> 0).toNumber() : message.x;
            if (message.low != null && message.hasOwnProperty("low"))
                object.low = options.json && !isFinite(message.low) ? String(message.low) : message.low;
            if (message.high != null && message.hasOwnProperty("high"))
                object.high = options.json && !isFinite(message.high) ? String(message.high) : message.high;
            return object;
        };

        /**
         * Converts this AreaRangePoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.AreaRangePoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        AreaRangePoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for AreaRangePoint
         * @function getTypeUrl
         * @memberof epoch_proto.AreaRangePoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        AreaRangePoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.AreaRangePoint";
        };

        return AreaRangePoint;
    })();

    epoch_proto.NumericAreaRangePoint = (function() {

        /**
         * Properties of a NumericAreaRangePoint.
         * @memberof epoch_proto
         * @interface INumericAreaRangePoint
         * @property {number|null} [x] NumericAreaRangePoint x
         * @property {number|null} [low] NumericAreaRangePoint low
         * @property {number|null} [high] NumericAreaRangePoint high
         */

        /**
         * Constructs a new NumericAreaRangePoint.
         * @memberof epoch_proto
         * @classdesc Represents a NumericAreaRangePoint.
         * @implements INumericAreaRangePoint
         * @constructor
         * @param {epoch_proto.INumericAreaRangePoint=} [properties] Properties to set
         */
        function NumericAreaRangePoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NumericAreaRangePoint x.
         * @member {number} x
         * @memberof epoch_proto.NumericAreaRangePoint
         * @instance
         */
        NumericAreaRangePoint.prototype.x = 0;

        /**
         * NumericAreaRangePoint low.
         * @member {number} low
         * @memberof epoch_proto.NumericAreaRangePoint
         * @instance
         */
        NumericAreaRangePoint.prototype.low = 0;

        /**
         * NumericAreaRangePoint high.
         * @member {number} high
         * @memberof epoch_proto.NumericAreaRangePoint
         * @instance
         */
        NumericAreaRangePoint.prototype.high = 0;

        /**
         * Creates a new NumericAreaRangePoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.NumericAreaRangePoint
         * @static
         * @param {epoch_proto.INumericAreaRangePoint=} [properties] Properties to set
         * @returns {epoch_proto.NumericAreaRangePoint} NumericAreaRangePoint instance
         */
        NumericAreaRangePoint.create = function create(properties) {
            return new NumericAreaRangePoint(properties);
        };

        /**
         * Encodes the specified NumericAreaRangePoint message. Does not implicitly {@link epoch_proto.NumericAreaRangePoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.NumericAreaRangePoint
         * @static
         * @param {epoch_proto.INumericAreaRangePoint} message NumericAreaRangePoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericAreaRangePoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 1 =*/9).double(message.x);
            if (message.low != null && Object.hasOwnProperty.call(message, "low"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.low);
            if (message.high != null && Object.hasOwnProperty.call(message, "high"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.high);
            return writer;
        };

        /**
         * Encodes the specified NumericAreaRangePoint message, length delimited. Does not implicitly {@link epoch_proto.NumericAreaRangePoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.NumericAreaRangePoint
         * @static
         * @param {epoch_proto.INumericAreaRangePoint} message NumericAreaRangePoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericAreaRangePoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NumericAreaRangePoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.NumericAreaRangePoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.NumericAreaRangePoint} NumericAreaRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericAreaRangePoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.NumericAreaRangePoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.double();
                        break;
                    }
                case 2: {
                        message.low = reader.double();
                        break;
                    }
                case 3: {
                        message.high = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NumericAreaRangePoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.NumericAreaRangePoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.NumericAreaRangePoint} NumericAreaRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericAreaRangePoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NumericAreaRangePoint message.
         * @function verify
         * @memberof epoch_proto.NumericAreaRangePoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NumericAreaRangePoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x !== "number")
                    return "x: number expected";
            if (message.low != null && message.hasOwnProperty("low"))
                if (typeof message.low !== "number")
                    return "low: number expected";
            if (message.high != null && message.hasOwnProperty("high"))
                if (typeof message.high !== "number")
                    return "high: number expected";
            return null;
        };

        /**
         * Creates a NumericAreaRangePoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.NumericAreaRangePoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.NumericAreaRangePoint} NumericAreaRangePoint
         */
        NumericAreaRangePoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.NumericAreaRangePoint)
                return object;
            let message = new $root.epoch_proto.NumericAreaRangePoint();
            if (object.x != null)
                message.x = Number(object.x);
            if (object.low != null)
                message.low = Number(object.low);
            if (object.high != null)
                message.high = Number(object.high);
            return message;
        };

        /**
         * Creates a plain object from a NumericAreaRangePoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.NumericAreaRangePoint
         * @static
         * @param {epoch_proto.NumericAreaRangePoint} message NumericAreaRangePoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NumericAreaRangePoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.x = 0;
                object.low = 0;
                object.high = 0;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                object.x = options.json && !isFinite(message.x) ? String(message.x) : message.x;
            if (message.low != null && message.hasOwnProperty("low"))
                object.low = options.json && !isFinite(message.low) ? String(message.low) : message.low;
            if (message.high != null && message.hasOwnProperty("high"))
                object.high = options.json && !isFinite(message.high) ? String(message.high) : message.high;
            return object;
        };

        /**
         * Converts this NumericAreaRangePoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.NumericAreaRangePoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NumericAreaRangePoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NumericAreaRangePoint
         * @function getTypeUrl
         * @memberof epoch_proto.NumericAreaRangePoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NumericAreaRangePoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.NumericAreaRangePoint";
        };

        return NumericAreaRangePoint;
    })();

    epoch_proto.AreaRangeSeries = (function() {

        /**
         * Properties of an AreaRangeSeries.
         * @memberof epoch_proto
         * @interface IAreaRangeSeries
         * @property {string|null} [name] AreaRangeSeries name
         * @property {Array.<epoch_proto.IAreaRangePoint>|null} [data] AreaRangeSeries data
         * @property {string|null} [fillColor] AreaRangeSeries fillColor
         * @property {number|null} [fillOpacity] AreaRangeSeries fillOpacity
         */

        /**
         * Constructs a new AreaRangeSeries.
         * @memberof epoch_proto
         * @classdesc Represents an AreaRangeSeries.
         * @implements IAreaRangeSeries
         * @constructor
         * @param {epoch_proto.IAreaRangeSeries=} [properties] Properties to set
         */
        function AreaRangeSeries(properties) {
            this.data = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * AreaRangeSeries name.
         * @member {string} name
         * @memberof epoch_proto.AreaRangeSeries
         * @instance
         */
        AreaRangeSeries.prototype.name = "";

        /**
         * AreaRangeSeries data.
         * @member {Array.<epoch_proto.IAreaRangePoint>} data
         * @memberof epoch_proto.AreaRangeSeries
         * @instance
         */
        AreaRangeSeries.prototype.data = $util.emptyArray;

        /**
         * AreaRangeSeries fillColor.
         * @member {string|null|undefined} fillColor
         * @memberof epoch_proto.AreaRangeSeries
         * @instance
         */
        AreaRangeSeries.prototype.fillColor = null;

        /**
         * AreaRangeSeries fillOpacity.
         * @member {number|null|undefined} fillOpacity
         * @memberof epoch_proto.AreaRangeSeries
         * @instance
         */
        AreaRangeSeries.prototype.fillOpacity = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(AreaRangeSeries.prototype, "_fillColor", {
            get: $util.oneOfGetter($oneOfFields = ["fillColor"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(AreaRangeSeries.prototype, "_fillOpacity", {
            get: $util.oneOfGetter($oneOfFields = ["fillOpacity"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new AreaRangeSeries instance using the specified properties.
         * @function create
         * @memberof epoch_proto.AreaRangeSeries
         * @static
         * @param {epoch_proto.IAreaRangeSeries=} [properties] Properties to set
         * @returns {epoch_proto.AreaRangeSeries} AreaRangeSeries instance
         */
        AreaRangeSeries.create = function create(properties) {
            return new AreaRangeSeries(properties);
        };

        /**
         * Encodes the specified AreaRangeSeries message. Does not implicitly {@link epoch_proto.AreaRangeSeries.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.AreaRangeSeries
         * @static
         * @param {epoch_proto.IAreaRangeSeries} message AreaRangeSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AreaRangeSeries.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.name);
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.AreaRangePoint.encode(message.data[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.fillColor != null && Object.hasOwnProperty.call(message, "fillColor"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.fillColor);
            if (message.fillOpacity != null && Object.hasOwnProperty.call(message, "fillOpacity"))
                writer.uint32(/* id 4, wireType 1 =*/33).double(message.fillOpacity);
            return writer;
        };

        /**
         * Encodes the specified AreaRangeSeries message, length delimited. Does not implicitly {@link epoch_proto.AreaRangeSeries.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.AreaRangeSeries
         * @static
         * @param {epoch_proto.IAreaRangeSeries} message AreaRangeSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AreaRangeSeries.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an AreaRangeSeries message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.AreaRangeSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.AreaRangeSeries} AreaRangeSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AreaRangeSeries.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.AreaRangeSeries();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.name = reader.string();
                        break;
                    }
                case 2: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.AreaRangePoint.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.fillColor = reader.string();
                        break;
                    }
                case 4: {
                        message.fillOpacity = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an AreaRangeSeries message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.AreaRangeSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.AreaRangeSeries} AreaRangeSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AreaRangeSeries.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an AreaRangeSeries message.
         * @function verify
         * @memberof epoch_proto.AreaRangeSeries
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        AreaRangeSeries.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.AreaRangePoint.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            if (message.fillColor != null && message.hasOwnProperty("fillColor")) {
                properties._fillColor = 1;
                if (!$util.isString(message.fillColor))
                    return "fillColor: string expected";
            }
            if (message.fillOpacity != null && message.hasOwnProperty("fillOpacity")) {
                properties._fillOpacity = 1;
                if (typeof message.fillOpacity !== "number")
                    return "fillOpacity: number expected";
            }
            return null;
        };

        /**
         * Creates an AreaRangeSeries message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.AreaRangeSeries
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.AreaRangeSeries} AreaRangeSeries
         */
        AreaRangeSeries.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.AreaRangeSeries)
                return object;
            let message = new $root.epoch_proto.AreaRangeSeries();
            if (object.name != null)
                message.name = String(object.name);
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.AreaRangeSeries.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.AreaRangeSeries.data: object expected");
                    message.data[i] = $root.epoch_proto.AreaRangePoint.fromObject(object.data[i]);
                }
            }
            if (object.fillColor != null)
                message.fillColor = String(object.fillColor);
            if (object.fillOpacity != null)
                message.fillOpacity = Number(object.fillOpacity);
            return message;
        };

        /**
         * Creates a plain object from an AreaRangeSeries message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.AreaRangeSeries
         * @static
         * @param {epoch_proto.AreaRangeSeries} message AreaRangeSeries
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        AreaRangeSeries.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.data = [];
            if (options.defaults)
                object.name = "";
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.AreaRangePoint.toObject(message.data[j], options);
            }
            if (message.fillColor != null && message.hasOwnProperty("fillColor")) {
                object.fillColor = message.fillColor;
                if (options.oneofs)
                    object._fillColor = "fillColor";
            }
            if (message.fillOpacity != null && message.hasOwnProperty("fillOpacity")) {
                object.fillOpacity = options.json && !isFinite(message.fillOpacity) ? String(message.fillOpacity) : message.fillOpacity;
                if (options.oneofs)
                    object._fillOpacity = "fillOpacity";
            }
            return object;
        };

        /**
         * Converts this AreaRangeSeries to JSON.
         * @function toJSON
         * @memberof epoch_proto.AreaRangeSeries
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        AreaRangeSeries.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for AreaRangeSeries
         * @function getTypeUrl
         * @memberof epoch_proto.AreaRangeSeries
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        AreaRangeSeries.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.AreaRangeSeries";
        };

        return AreaRangeSeries;
    })();

    epoch_proto.AreaRangeDef = (function() {

        /**
         * Properties of an AreaRangeDef.
         * @memberof epoch_proto
         * @interface IAreaRangeDef
         * @property {epoch_proto.IChartDef|null} [chartDef] AreaRangeDef chartDef
         * @property {Array.<epoch_proto.IAreaRangeSeries>|null} [series] AreaRangeDef series
         * @property {epoch_proto.ILine|null} [centerLine] AreaRangeDef centerLine
         */

        /**
         * Constructs a new AreaRangeDef.
         * @memberof epoch_proto
         * @classdesc Represents an AreaRangeDef.
         * @implements IAreaRangeDef
         * @constructor
         * @param {epoch_proto.IAreaRangeDef=} [properties] Properties to set
         */
        function AreaRangeDef(properties) {
            this.series = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * AreaRangeDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.AreaRangeDef
         * @instance
         */
        AreaRangeDef.prototype.chartDef = null;

        /**
         * AreaRangeDef series.
         * @member {Array.<epoch_proto.IAreaRangeSeries>} series
         * @memberof epoch_proto.AreaRangeDef
         * @instance
         */
        AreaRangeDef.prototype.series = $util.emptyArray;

        /**
         * AreaRangeDef centerLine.
         * @member {epoch_proto.ILine|null|undefined} centerLine
         * @memberof epoch_proto.AreaRangeDef
         * @instance
         */
        AreaRangeDef.prototype.centerLine = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(AreaRangeDef.prototype, "_centerLine", {
            get: $util.oneOfGetter($oneOfFields = ["centerLine"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new AreaRangeDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.AreaRangeDef
         * @static
         * @param {epoch_proto.IAreaRangeDef=} [properties] Properties to set
         * @returns {epoch_proto.AreaRangeDef} AreaRangeDef instance
         */
        AreaRangeDef.create = function create(properties) {
            return new AreaRangeDef(properties);
        };

        /**
         * Encodes the specified AreaRangeDef message. Does not implicitly {@link epoch_proto.AreaRangeDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.AreaRangeDef
         * @static
         * @param {epoch_proto.IAreaRangeDef} message AreaRangeDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AreaRangeDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.series != null && message.series.length)
                for (let i = 0; i < message.series.length; ++i)
                    $root.epoch_proto.AreaRangeSeries.encode(message.series[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.centerLine != null && Object.hasOwnProperty.call(message, "centerLine"))
                $root.epoch_proto.Line.encode(message.centerLine, writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified AreaRangeDef message, length delimited. Does not implicitly {@link epoch_proto.AreaRangeDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.AreaRangeDef
         * @static
         * @param {epoch_proto.IAreaRangeDef} message AreaRangeDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        AreaRangeDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an AreaRangeDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.AreaRangeDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.AreaRangeDef} AreaRangeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AreaRangeDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.AreaRangeDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.series && message.series.length))
                            message.series = [];
                        message.series.push($root.epoch_proto.AreaRangeSeries.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.centerLine = $root.epoch_proto.Line.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an AreaRangeDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.AreaRangeDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.AreaRangeDef} AreaRangeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        AreaRangeDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an AreaRangeDef message.
         * @function verify
         * @memberof epoch_proto.AreaRangeDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        AreaRangeDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.series != null && message.hasOwnProperty("series")) {
                if (!Array.isArray(message.series))
                    return "series: array expected";
                for (let i = 0; i < message.series.length; ++i) {
                    let error = $root.epoch_proto.AreaRangeSeries.verify(message.series[i]);
                    if (error)
                        return "series." + error;
                }
            }
            if (message.centerLine != null && message.hasOwnProperty("centerLine")) {
                properties._centerLine = 1;
                {
                    let error = $root.epoch_proto.Line.verify(message.centerLine);
                    if (error)
                        return "centerLine." + error;
                }
            }
            return null;
        };

        /**
         * Creates an AreaRangeDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.AreaRangeDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.AreaRangeDef} AreaRangeDef
         */
        AreaRangeDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.AreaRangeDef)
                return object;
            let message = new $root.epoch_proto.AreaRangeDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.AreaRangeDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.series) {
                if (!Array.isArray(object.series))
                    throw TypeError(".epoch_proto.AreaRangeDef.series: array expected");
                message.series = [];
                for (let i = 0; i < object.series.length; ++i) {
                    if (typeof object.series[i] !== "object")
                        throw TypeError(".epoch_proto.AreaRangeDef.series: object expected");
                    message.series[i] = $root.epoch_proto.AreaRangeSeries.fromObject(object.series[i]);
                }
            }
            if (object.centerLine != null) {
                if (typeof object.centerLine !== "object")
                    throw TypeError(".epoch_proto.AreaRangeDef.centerLine: object expected");
                message.centerLine = $root.epoch_proto.Line.fromObject(object.centerLine);
            }
            return message;
        };

        /**
         * Creates a plain object from an AreaRangeDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.AreaRangeDef
         * @static
         * @param {epoch_proto.AreaRangeDef} message AreaRangeDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        AreaRangeDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.series = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.series && message.series.length) {
                object.series = [];
                for (let j = 0; j < message.series.length; ++j)
                    object.series[j] = $root.epoch_proto.AreaRangeSeries.toObject(message.series[j], options);
            }
            if (message.centerLine != null && message.hasOwnProperty("centerLine")) {
                object.centerLine = $root.epoch_proto.Line.toObject(message.centerLine, options);
                if (options.oneofs)
                    object._centerLine = "centerLine";
            }
            return object;
        };

        /**
         * Converts this AreaRangeDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.AreaRangeDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        AreaRangeDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for AreaRangeDef
         * @function getTypeUrl
         * @memberof epoch_proto.AreaRangeDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        AreaRangeDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.AreaRangeDef";
        };

        return AreaRangeDef;
    })();

    epoch_proto.GaugeStop = (function() {

        /**
         * Properties of a GaugeStop.
         * @memberof epoch_proto
         * @interface IGaugeStop
         * @property {number|null} [position] GaugeStop position
         * @property {string|null} [color] GaugeStop color
         */

        /**
         * Constructs a new GaugeStop.
         * @memberof epoch_proto
         * @classdesc Represents a GaugeStop.
         * @implements IGaugeStop
         * @constructor
         * @param {epoch_proto.IGaugeStop=} [properties] Properties to set
         */
        function GaugeStop(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * GaugeStop position.
         * @member {number} position
         * @memberof epoch_proto.GaugeStop
         * @instance
         */
        GaugeStop.prototype.position = 0;

        /**
         * GaugeStop color.
         * @member {string} color
         * @memberof epoch_proto.GaugeStop
         * @instance
         */
        GaugeStop.prototype.color = "";

        /**
         * Creates a new GaugeStop instance using the specified properties.
         * @function create
         * @memberof epoch_proto.GaugeStop
         * @static
         * @param {epoch_proto.IGaugeStop=} [properties] Properties to set
         * @returns {epoch_proto.GaugeStop} GaugeStop instance
         */
        GaugeStop.create = function create(properties) {
            return new GaugeStop(properties);
        };

        /**
         * Encodes the specified GaugeStop message. Does not implicitly {@link epoch_proto.GaugeStop.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.GaugeStop
         * @static
         * @param {epoch_proto.IGaugeStop} message GaugeStop message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        GaugeStop.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.position != null && Object.hasOwnProperty.call(message, "position"))
                writer.uint32(/* id 1, wireType 1 =*/9).double(message.position);
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.color);
            return writer;
        };

        /**
         * Encodes the specified GaugeStop message, length delimited. Does not implicitly {@link epoch_proto.GaugeStop.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.GaugeStop
         * @static
         * @param {epoch_proto.IGaugeStop} message GaugeStop message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        GaugeStop.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a GaugeStop message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.GaugeStop
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.GaugeStop} GaugeStop
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        GaugeStop.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.GaugeStop();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.position = reader.double();
                        break;
                    }
                case 2: {
                        message.color = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a GaugeStop message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.GaugeStop
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.GaugeStop} GaugeStop
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        GaugeStop.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a GaugeStop message.
         * @function verify
         * @memberof epoch_proto.GaugeStop
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        GaugeStop.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.position != null && message.hasOwnProperty("position"))
                if (typeof message.position !== "number")
                    return "position: number expected";
            if (message.color != null && message.hasOwnProperty("color"))
                if (!$util.isString(message.color))
                    return "color: string expected";
            return null;
        };

        /**
         * Creates a GaugeStop message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.GaugeStop
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.GaugeStop} GaugeStop
         */
        GaugeStop.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.GaugeStop)
                return object;
            let message = new $root.epoch_proto.GaugeStop();
            if (object.position != null)
                message.position = Number(object.position);
            if (object.color != null)
                message.color = String(object.color);
            return message;
        };

        /**
         * Creates a plain object from a GaugeStop message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.GaugeStop
         * @static
         * @param {epoch_proto.GaugeStop} message GaugeStop
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        GaugeStop.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.position = 0;
                object.color = "";
            }
            if (message.position != null && message.hasOwnProperty("position"))
                object.position = options.json && !isFinite(message.position) ? String(message.position) : message.position;
            if (message.color != null && message.hasOwnProperty("color"))
                object.color = message.color;
            return object;
        };

        /**
         * Converts this GaugeStop to JSON.
         * @function toJSON
         * @memberof epoch_proto.GaugeStop
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        GaugeStop.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for GaugeStop
         * @function getTypeUrl
         * @memberof epoch_proto.GaugeStop
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        GaugeStop.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.GaugeStop";
        };

        return GaugeStop;
    })();

    epoch_proto.GaugeDef = (function() {

        /**
         * Properties of a GaugeDef.
         * @memberof epoch_proto
         * @interface IGaugeDef
         * @property {epoch_proto.IChartDef|null} [chartDef] GaugeDef chartDef
         * @property {number|null} [value] GaugeDef value
         * @property {number|null} [min] GaugeDef min
         * @property {number|null} [max] GaugeDef max
         * @property {string|null} [valueSuffix] GaugeDef valueSuffix
         * @property {Array.<epoch_proto.IGaugeStop>|null} [stops] GaugeDef stops
         * @property {boolean|null} [solid] GaugeDef solid
         */

        /**
         * Constructs a new GaugeDef.
         * @memberof epoch_proto
         * @classdesc Represents a GaugeDef.
         * @implements IGaugeDef
         * @constructor
         * @param {epoch_proto.IGaugeDef=} [properties] Properties to set
         */
        function GaugeDef(properties) {
            this.stops = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * GaugeDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.GaugeDef
         * @instance
         */
        GaugeDef.prototype.chartDef = null;

        /**
         * GaugeDef value.
         * @member {number} value
         * @memberof epoch_proto.GaugeDef
         * @instance
         */
        GaugeDef.prototype.value = 0;

        /**
         * GaugeDef min.
         * @member {number} min
         * @memberof epoch_proto.GaugeDef
         * @instance
         */
        GaugeDef.prototype.min = 0;

        /**
         * GaugeDef max.
         * @member {number} max
         * @memberof epoch_proto.GaugeDef
         * @instance
         */
        GaugeDef.prototype.max = 0;

        /**
         * GaugeDef valueSuffix.
         * @member {string|null|undefined} valueSuffix
         * @memberof epoch_proto.GaugeDef
         * @instance
         */
        GaugeDef.prototype.valueSuffix = null;

        /**
         * GaugeDef stops.
         * @member {Array.<epoch_proto.IGaugeStop>} stops
         * @memberof epoch_proto.GaugeDef
         * @instance
         */
        GaugeDef.prototype.stops = $util.emptyArray;

        /**
         * GaugeDef solid.
         * @member {boolean} solid
         * @memberof epoch_proto.GaugeDef
         * @instance
         */
        GaugeDef.prototype.solid = false;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(GaugeDef.prototype, "_valueSuffix", {
            get: $util.oneOfGetter($oneOfFields = ["valueSuffix"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new GaugeDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.GaugeDef
         * @static
         * @param {epoch_proto.IGaugeDef=} [properties] Properties to set
         * @returns {epoch_proto.GaugeDef} GaugeDef instance
         */
        GaugeDef.create = function create(properties) {
            return new GaugeDef(properties);
        };

        /**
         * Encodes the specified GaugeDef message. Does not implicitly {@link epoch_proto.GaugeDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.GaugeDef
         * @static
         * @param {epoch_proto.IGaugeDef} message GaugeDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        GaugeDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.value != null && Object.hasOwnProperty.call(message, "value"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.value);
            if (message.min != null && Object.hasOwnProperty.call(message, "min"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.min);
            if (message.max != null && Object.hasOwnProperty.call(message, "max"))
                writer.uint32(/* id 4, wireType 1 =*/33).double(message.max);
            if (message.valueSuffix != null && Object.hasOwnProperty.call(message, "valueSuffix"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.valueSuffix);
            if (message.stops != null && message.stops.length)
                for (let i = 0; i < message.stops.length; ++i)
                    $root.epoch_proto.GaugeStop.encode(message.stops[i], writer.uint32(/* id 6, wireType 2 =*/50).fork()).ldelim();
            if (message.solid != null && Object.hasOwnProperty.call(message, "solid"))
                writer.uint32(/* id 7, wireType 0 =*/56).bool(message.solid);
            return writer;
        };

        /**
         * Encodes the specified GaugeDef message, length delimited. Does not implicitly {@link epoch_proto.GaugeDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.GaugeDef
         * @static
         * @param {epoch_proto.IGaugeDef} message GaugeDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        GaugeDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a GaugeDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.GaugeDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.GaugeDef} GaugeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        GaugeDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.GaugeDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        message.value = reader.double();
                        break;
                    }
                case 3: {
                        message.min = reader.double();
                        break;
                    }
                case 4: {
                        message.max = reader.double();
                        break;
                    }
                case 5: {
                        message.valueSuffix = reader.string();
                        break;
                    }
                case 6: {
                        if (!(message.stops && message.stops.length))
                            message.stops = [];
                        message.stops.push($root.epoch_proto.GaugeStop.decode(reader, reader.uint32()));
                        break;
                    }
                case 7: {
                        message.solid = reader.bool();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a GaugeDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.GaugeDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.GaugeDef} GaugeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        GaugeDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a GaugeDef message.
         * @function verify
         * @memberof epoch_proto.GaugeDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        GaugeDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.value != null && message.hasOwnProperty("value"))
                if (typeof message.value !== "number")
                    return "value: number expected";
            if (message.min != null && message.hasOwnProperty("min"))
                if (typeof message.min !== "number")
                    return "min: number expected";
            if (message.max != null && message.hasOwnProperty("max"))
                if (typeof message.max !== "number")
                    return "max: number expected";
            if (message.valueSuffix != null && message.hasOwnProperty("valueSuffix")) {
                properties._valueSuffix = 1;
                if (!$util.isString(message.valueSuffix))
                    return "valueSuffix: string expected";
            }
            if (message.stops != null && message.hasOwnProperty("stops")) {
                if (!Array.isArray(message.stops))
                    return "stops: array expected";
                for (let i = 0; i < message.stops.length; ++i) {
                    let error = $root.epoch_proto.GaugeStop.verify(message.stops[i]);
                    if (error)
                        return "stops." + error;
                }
            }
            if (message.solid != null && message.hasOwnProperty("solid"))
                if (typeof message.solid !== "boolean")
                    return "solid: boolean expected";
            return null;
        };

        /**
         * Creates a GaugeDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.GaugeDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.GaugeDef} GaugeDef
         */
        GaugeDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.GaugeDef)
                return object;
            let message = new $root.epoch_proto.GaugeDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.GaugeDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.value != null)
                message.value = Number(object.value);
            if (object.min != null)
                message.min = Number(object.min);
            if (object.max != null)
                message.max = Number(object.max);
            if (object.valueSuffix != null)
                message.valueSuffix = String(object.valueSuffix);
            if (object.stops) {
                if (!Array.isArray(object.stops))
                    throw TypeError(".epoch_proto.GaugeDef.stops: array expected");
                message.stops = [];
                for (let i = 0; i < object.stops.length; ++i) {
                    if (typeof object.stops[i] !== "object")
                        throw TypeError(".epoch_proto.GaugeDef.stops: object expected");
                    message.stops[i] = $root.epoch_proto.GaugeStop.fromObject(object.stops[i]);
                }
            }
            if (object.solid != null)
                message.solid = Boolean(object.solid);
            return message;
        };

        /**
         * Creates a plain object from a GaugeDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.GaugeDef
         * @static
         * @param {epoch_proto.GaugeDef} message GaugeDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        GaugeDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.stops = [];
            if (options.defaults) {
                object.chartDef = null;
                object.value = 0;
                object.min = 0;
                object.max = 0;
                object.solid = false;
            }
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.value != null && message.hasOwnProperty("value"))
                object.value = options.json && !isFinite(message.value) ? String(message.value) : message.value;
            if (message.min != null && message.hasOwnProperty("min"))
                object.min = options.json && !isFinite(message.min) ? String(message.min) : message.min;
            if (message.max != null && message.hasOwnProperty("max"))
                object.max = options.json && !isFinite(message.max) ? String(message.max) : message.max;
            if (message.valueSuffix != null && message.hasOwnProperty("valueSuffix")) {
                object.valueSuffix = message.valueSuffix;
                if (options.oneofs)
                    object._valueSuffix = "valueSuffix";
            }
            if (message.stops && message.stops.length) {
                object.stops = [];
                for (let j = 0; j < message.stops.length; ++j)
                    object.stops[j] = $root.epoch_proto.GaugeStop.toObject(message.stops[j], options);
            }
            if (message.solid != null && message.hasOwnProperty("solid"))
                object.solid = message.solid;
            return object;
        };

        /**
         * Converts this GaugeDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.GaugeDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        GaugeDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for GaugeDef
         * @function getTypeUrl
         * @memberof epoch_proto.GaugeDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        GaugeDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.GaugeDef";
        };

        return GaugeDef;
    })();

    epoch_proto.BulletRange = (function() {

        /**
         * Properties of a BulletRange.
         * @memberof epoch_proto
         * @interface IBulletRange
         * @property {number|null} [from] BulletRange from
         * @property {number|null} [to] BulletRange to
         * @property {string|null} [color] BulletRange color
         */

        /**
         * Constructs a new BulletRange.
         * @memberof epoch_proto
         * @classdesc Represents a BulletRange.
         * @implements IBulletRange
         * @constructor
         * @param {epoch_proto.IBulletRange=} [properties] Properties to set
         */
        function BulletRange(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BulletRange from.
         * @member {number} from
         * @memberof epoch_proto.BulletRange
         * @instance
         */
        BulletRange.prototype.from = 0;

        /**
         * BulletRange to.
         * @member {number} to
         * @memberof epoch_proto.BulletRange
         * @instance
         */
        BulletRange.prototype.to = 0;

        /**
         * BulletRange color.
         * @member {string} color
         * @memberof epoch_proto.BulletRange
         * @instance
         */
        BulletRange.prototype.color = "";

        /**
         * Creates a new BulletRange instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BulletRange
         * @static
         * @param {epoch_proto.IBulletRange=} [properties] Properties to set
         * @returns {epoch_proto.BulletRange} BulletRange instance
         */
        BulletRange.create = function create(properties) {
            return new BulletRange(properties);
        };

        /**
         * Encodes the specified BulletRange message. Does not implicitly {@link epoch_proto.BulletRange.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BulletRange
         * @static
         * @param {epoch_proto.IBulletRange} message BulletRange message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BulletRange.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.from != null && Object.hasOwnProperty.call(message, "from"))
                writer.uint32(/* id 1, wireType 1 =*/9).double(message.from);
            if (message.to != null && Object.hasOwnProperty.call(message, "to"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.to);
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.color);
            return writer;
        };

        /**
         * Encodes the specified BulletRange message, length delimited. Does not implicitly {@link epoch_proto.BulletRange.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BulletRange
         * @static
         * @param {epoch_proto.IBulletRange} message BulletRange message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BulletRange.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BulletRange message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BulletRange
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BulletRange} BulletRange
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BulletRange.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BulletRange();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.from = reader.double();
                        break;
                    }
                case 2: {
                        message.to = reader.double();
                        break;
                    }
                case 3: {
                        message.color = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BulletRange message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BulletRange
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BulletRange} BulletRange
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BulletRange.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BulletRange message.
         * @function verify
         * @memberof epoch_proto.BulletRange
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BulletRange.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.from != null && message.hasOwnProperty("from"))
                if (typeof message.from !== "number")
                    return "from: number expected";
            if (message.to != null && message.hasOwnProperty("to"))
                if (typeof message.to !== "number")
                    return "to: number expected";
            if (message.color != null && message.hasOwnProperty("color"))
                if (!$util.isString(message.color))
                    return "color: string expected";
            return null;
        };

        /**
         * Creates a BulletRange message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BulletRange
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BulletRange} BulletRange
         */
        BulletRange.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BulletRange)
                return object;
            let message = new $root.epoch_proto.BulletRange();
            if (object.from != null)
                message.from = Number(object.from);
            if (object.to != null)
                message.to = Number(object.to);
            if (object.color != null)
                message.color = String(object.color);
            return message;
        };

        /**
         * Creates a plain object from a BulletRange message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BulletRange
         * @static
         * @param {epoch_proto.BulletRange} message BulletRange
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BulletRange.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.from = 0;
                object.to = 0;
                object.color = "";
            }
            if (message.from != null && message.hasOwnProperty("from"))
                object.from = options.json && !isFinite(message.from) ? String(message.from) : message.from;
            if (message.to != null && message.hasOwnProperty("to"))
                object.to = options.json && !isFinite(message.to) ? String(message.to) : message.to;
            if (message.color != null && message.hasOwnProperty("color"))
                object.color = message.color;
            return object;
        };

        /**
         * Converts this BulletRange to JSON.
         * @function toJSON
         * @memberof epoch_proto.BulletRange
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BulletRange.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BulletRange
         * @function getTypeUrl
         * @memberof epoch_proto.BulletRange
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BulletRange.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BulletRange";
        };

        return BulletRange;
    })();

    epoch_proto.BulletDef = (function() {

        /**
         * Properties of a BulletDef.
         * @memberof epoch_proto
         * @interface IBulletDef
         * @property {epoch_proto.IChartDef|null} [chartDef] BulletDef chartDef
         * @property {number|null} [value] BulletDef value
         * @property {number|null} [target] BulletDef target
         * @property {Array.<epoch_proto.IBulletRange>|null} [ranges] BulletDef ranges
         */

        /**
         * Constructs a new BulletDef.
         * @memberof epoch_proto
         * @classdesc Represents a BulletDef.
         * @implements IBulletDef
         * @constructor
         * @param {epoch_proto.IBulletDef=} [properties] Properties to set
         */
        function BulletDef(properties) {
            this.ranges = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BulletDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.BulletDef
         * @instance
         */
        BulletDef.prototype.chartDef = null;

        /**
         * BulletDef value.
         * @member {number} value
         * @memberof epoch_proto.BulletDef
         * @instance
         */
        BulletDef.prototype.value = 0;

        /**
         * BulletDef target.
         * @member {number} target
         * @memberof epoch_proto.BulletDef
         * @instance
         */
        BulletDef.prototype.target = 0;

        /**
         * BulletDef ranges.
         * @member {Array.<epoch_proto.IBulletRange>} ranges
         * @memberof epoch_proto.BulletDef
         * @instance
         */
        BulletDef.prototype.ranges = $util.emptyArray;

        /**
         * Creates a new BulletDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BulletDef
         * @static
         * @param {epoch_proto.IBulletDef=} [properties] Properties to set
         * @returns {epoch_proto.BulletDef} BulletDef instance
         */
        BulletDef.create = function create(properties) {
            return new BulletDef(properties);
        };

        /**
         * Encodes the specified BulletDef message. Does not implicitly {@link epoch_proto.BulletDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BulletDef
         * @static
         * @param {epoch_proto.IBulletDef} message BulletDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BulletDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.value != null && Object.hasOwnProperty.call(message, "value"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.value);
            if (message.target != null && Object.hasOwnProperty.call(message, "target"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.target);
            if (message.ranges != null && message.ranges.length)
                for (let i = 0; i < message.ranges.length; ++i)
                    $root.epoch_proto.BulletRange.encode(message.ranges[i], writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified BulletDef message, length delimited. Does not implicitly {@link epoch_proto.BulletDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BulletDef
         * @static
         * @param {epoch_proto.IBulletDef} message BulletDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BulletDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BulletDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BulletDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BulletDef} BulletDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BulletDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BulletDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        message.value = reader.double();
                        break;
                    }
                case 3: {
                        message.target = reader.double();
                        break;
                    }
                case 4: {
                        if (!(message.ranges && message.ranges.length))
                            message.ranges = [];
                        message.ranges.push($root.epoch_proto.BulletRange.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BulletDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BulletDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BulletDef} BulletDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BulletDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BulletDef message.
         * @function verify
         * @memberof epoch_proto.BulletDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BulletDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.value != null && message.hasOwnProperty("value"))
                if (typeof message.value !== "number")
                    return "value: number expected";
            if (message.target != null && message.hasOwnProperty("target"))
                if (typeof message.target !== "number")
                    return "target: number expected";
            if (message.ranges != null && message.hasOwnProperty("ranges")) {
                if (!Array.isArray(message.ranges))
                    return "ranges: array expected";
                for (let i = 0; i < message.ranges.length; ++i) {
                    let error = $root.epoch_proto.BulletRange.verify(message.ranges[i]);
                    if (error)
                        return "ranges." + error;
                }
            }
            return null;
        };

        /**
         * Creates a BulletDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BulletDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BulletDef} BulletDef
         */
        BulletDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BulletDef)
                return object;
            let message = new $root.epoch_proto.BulletDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.BulletDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.value != null)
                message.value = Number(object.value);
            if (object.target != null)
                message.target = Number(object.target);
            if (object.ranges) {
                if (!Array.isArray(object.ranges))
                    throw TypeError(".epoch_proto.BulletDef.ranges: array expected");
                message.ranges = [];
                for (let i = 0; i < object.ranges.length; ++i) {
                    if (typeof object.ranges[i] !== "object")
                        throw TypeError(".epoch_proto.BulletDef.ranges: object expected");
                    message.ranges[i] = $root.epoch_proto.BulletRange.fromObject(object.ranges[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a BulletDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BulletDef
         * @static
         * @param {epoch_proto.BulletDef} message BulletDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BulletDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.ranges = [];
            if (options.defaults) {
                object.chartDef = null;
                object.value = 0;
                object.target = 0;
            }
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.value != null && message.hasOwnProperty("value"))
                object.value = options.json && !isFinite(message.value) ? String(message.value) : message.value;
            if (message.target != null && message.hasOwnProperty("target"))
                object.target = options.json && !isFinite(message.target) ? String(message.target) : message.target;
            if (message.ranges && message.ranges.length) {
                object.ranges = [];
                for (let j = 0; j < message.ranges.length; ++j)
                    object.ranges[j] = $root.epoch_proto.BulletRange.toObject(message.ranges[j], options);
            }
            return object;
        };

        /**
         * Converts this BulletDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.BulletDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BulletDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BulletDef
         * @function getTypeUrl
         * @memberof epoch_proto.BulletDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BulletDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BulletDef";
        };

        return BulletDef;
    })();

    epoch_proto.TimelineEvent = (function() {

        /**
         * Properties of a TimelineEvent.
         * @memberof epoch_proto
         * @interface ITimelineEvent
         * @property {number|Long|null} [timestamp] TimelineEvent timestamp
         * @property {string|null} [name] TimelineEvent name
         * @property {string|null} [label] TimelineEvent label
         * @property {string|null} [description] TimelineEvent description
         * @property {string|null} [color] TimelineEvent color
         */

        /**
         * Constructs a new TimelineEvent.
         * @memberof epoch_proto
         * @classdesc Represents a TimelineEvent.
         * @implements ITimelineEvent
         * @constructor
         * @param {epoch_proto.ITimelineEvent=} [properties] Properties to set
         */
        function TimelineEvent(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * TimelineEvent timestamp.
         * @member {number|Long} timestamp
         * @memberof epoch_proto.TimelineEvent
         * @instance
         */
        TimelineEvent.prototype.timestamp = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * TimelineEvent name.
         * @member {string} name
         * @memberof epoch_proto.TimelineEvent
         * @instance
         */
        TimelineEvent.prototype.name = "";

        /**
         * TimelineEvent label.
         * @member {string|null|undefined} label
         * @memberof epoch_proto.TimelineEvent
         * @instance
         */
        TimelineEvent.prototype.label = null;

        /**
         * TimelineEvent description.
         * @member {string|null|undefined} description
         * @memberof epoch_proto.TimelineEvent
         * @instance
         */
        TimelineEvent.prototype.description = null;

        /**
         * TimelineEvent color.
         * @member {string|null|undefined} color
         * @memberof epoch_proto.TimelineEvent
         * @instance
         */
        TimelineEvent.prototype.color = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(TimelineEvent.prototype, "_label", {
            get: $util.oneOfGetter($oneOfFields = ["label"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(TimelineEvent.prototype, "_description", {
            get: $util.oneOfGetter($oneOfFields = ["description"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(TimelineEvent.prototype, "_color", {
            get: $util.oneOfGetter($oneOfFields = ["color"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new TimelineEvent instance using the specified properties.
         * @function create
         * @memberof epoch_proto.TimelineEvent
         * @static
         * @param {epoch_proto.ITimelineEvent=} [properties] Properties to set
         * @returns {epoch_proto.TimelineEvent} TimelineEvent instance
         */
        TimelineEvent.create = function create(properties) {
            return new TimelineEvent(properties);
        };

        /**
         * Encodes the specified TimelineEvent message. Does not implicitly {@link epoch_proto.TimelineEvent.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.TimelineEvent
         * @static
         * @param {epoch_proto.ITimelineEvent} message TimelineEvent message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TimelineEvent.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.timestamp != null && Object.hasOwnProperty.call(message, "timestamp"))
                writer.uint32(/* id 1, wireType 0 =*/8).int64(message.timestamp);
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 2, wireType 2 =*/18).string(message.name);
            if (message.label != null && Object.hasOwnProperty.call(message, "label"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.label);
            if (message.description != null && Object.hasOwnProperty.call(message, "description"))
                writer.uint32(/* id 4, wireType 2 =*/34).string(message.description);
            if (message.color != null && Object.hasOwnProperty.call(message, "color"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.color);
            return writer;
        };

        /**
         * Encodes the specified TimelineEvent message, length delimited. Does not implicitly {@link epoch_proto.TimelineEvent.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.TimelineEvent
         * @static
         * @param {epoch_proto.ITimelineEvent} message TimelineEvent message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TimelineEvent.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a TimelineEvent message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.TimelineEvent
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.TimelineEvent} TimelineEvent
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TimelineEvent.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.TimelineEvent();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.timestamp = reader.int64();
                        break;
                    }
                case 2: {
                        message.name = reader.string();
                        break;
                    }
                case 3: {
                        message.label = reader.string();
                        break;
                    }
                case 4: {
                        message.description = reader.string();
                        break;
                    }
                case 5: {
                        message.color = reader.string();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a TimelineEvent message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.TimelineEvent
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.TimelineEvent} TimelineEvent
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TimelineEvent.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a TimelineEvent message.
         * @function verify
         * @memberof epoch_proto.TimelineEvent
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        TimelineEvent.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.timestamp != null && message.hasOwnProperty("timestamp"))
                if (!$util.isInteger(message.timestamp) && !(message.timestamp && $util.isInteger(message.timestamp.low) && $util.isInteger(message.timestamp.high)))
                    return "timestamp: integer|Long expected";
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.label != null && message.hasOwnProperty("label")) {
                properties._label = 1;
                if (!$util.isString(message.label))
                    return "label: string expected";
            }
            if (message.description != null && message.hasOwnProperty("description")) {
                properties._description = 1;
                if (!$util.isString(message.description))
                    return "description: string expected";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                properties._color = 1;
                if (!$util.isString(message.color))
                    return "color: string expected";
            }
            return null;
        };

        /**
         * Creates a TimelineEvent message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.TimelineEvent
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.TimelineEvent} TimelineEvent
         */
        TimelineEvent.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.TimelineEvent)
                return object;
            let message = new $root.epoch_proto.TimelineEvent();
            if (object.timestamp != null)
                if ($util.Long)
                    (message.timestamp = $util.Long.fromValue(object.timestamp)).unsigned = false;
                else if (typeof object.timestamp === "string")
                    message.timestamp = parseInt(object.timestamp, 10);
                else if (typeof object.timestamp === "number")
                    message.timestamp = object.timestamp;
                else if (typeof object.timestamp === "object")
                    message.timestamp = new $util.LongBits(object.timestamp.low >>> 0, object.timestamp.high >>> 0).toNumber();
            if (object.name != null)
                message.name = String(object.name);
            if (object.label != null)
                message.label = String(object.label);
            if (object.description != null)
                message.description = String(object.description);
            if (object.color != null)
                message.color = String(object.color);
            return message;
        };

        /**
         * Creates a plain object from a TimelineEvent message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.TimelineEvent
         * @static
         * @param {epoch_proto.TimelineEvent} message TimelineEvent
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        TimelineEvent.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                if ($util.Long) {
                    let long = new $util.Long(0, 0, false);
                    object.timestamp = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.timestamp = options.longs === String ? "0" : 0;
                object.name = "";
            }
            if (message.timestamp != null && message.hasOwnProperty("timestamp"))
                if (typeof message.timestamp === "number")
                    object.timestamp = options.longs === String ? String(message.timestamp) : message.timestamp;
                else
                    object.timestamp = options.longs === String ? $util.Long.prototype.toString.call(message.timestamp) : options.longs === Number ? new $util.LongBits(message.timestamp.low >>> 0, message.timestamp.high >>> 0).toNumber() : message.timestamp;
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.label != null && message.hasOwnProperty("label")) {
                object.label = message.label;
                if (options.oneofs)
                    object._label = "label";
            }
            if (message.description != null && message.hasOwnProperty("description")) {
                object.description = message.description;
                if (options.oneofs)
                    object._description = "description";
            }
            if (message.color != null && message.hasOwnProperty("color")) {
                object.color = message.color;
                if (options.oneofs)
                    object._color = "color";
            }
            return object;
        };

        /**
         * Converts this TimelineEvent to JSON.
         * @function toJSON
         * @memberof epoch_proto.TimelineEvent
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        TimelineEvent.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for TimelineEvent
         * @function getTypeUrl
         * @memberof epoch_proto.TimelineEvent
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        TimelineEvent.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.TimelineEvent";
        };

        return TimelineEvent;
    })();

    epoch_proto.TimelineDef = (function() {

        /**
         * Properties of a TimelineDef.
         * @memberof epoch_proto
         * @interface ITimelineDef
         * @property {epoch_proto.IChartDef|null} [chartDef] TimelineDef chartDef
         * @property {Array.<epoch_proto.ITimelineEvent>|null} [events] TimelineDef events
         */

        /**
         * Constructs a new TimelineDef.
         * @memberof epoch_proto
         * @classdesc Represents a TimelineDef.
         * @implements ITimelineDef
         * @constructor
         * @param {epoch_proto.ITimelineDef=} [properties] Properties to set
         */
        function TimelineDef(properties) {
            this.events = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * TimelineDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.TimelineDef
         * @instance
         */
        TimelineDef.prototype.chartDef = null;

        /**
         * TimelineDef events.
         * @member {Array.<epoch_proto.ITimelineEvent>} events
         * @memberof epoch_proto.TimelineDef
         * @instance
         */
        TimelineDef.prototype.events = $util.emptyArray;

        /**
         * Creates a new TimelineDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.TimelineDef
         * @static
         * @param {epoch_proto.ITimelineDef=} [properties] Properties to set
         * @returns {epoch_proto.TimelineDef} TimelineDef instance
         */
        TimelineDef.create = function create(properties) {
            return new TimelineDef(properties);
        };

        /**
         * Encodes the specified TimelineDef message. Does not implicitly {@link epoch_proto.TimelineDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.TimelineDef
         * @static
         * @param {epoch_proto.ITimelineDef} message TimelineDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TimelineDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.events != null && message.events.length)
                for (let i = 0; i < message.events.length; ++i)
                    $root.epoch_proto.TimelineEvent.encode(message.events[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified TimelineDef message, length delimited. Does not implicitly {@link epoch_proto.TimelineDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.TimelineDef
         * @static
         * @param {epoch_proto.ITimelineDef} message TimelineDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TimelineDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a TimelineDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.TimelineDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.TimelineDef} TimelineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TimelineDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.TimelineDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.events && message.events.length))
                            message.events = [];
                        message.events.push($root.epoch_proto.TimelineEvent.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a TimelineDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.TimelineDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.TimelineDef} TimelineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TimelineDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a TimelineDef message.
         * @function verify
         * @memberof epoch_proto.TimelineDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        TimelineDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.events != null && message.hasOwnProperty("events")) {
                if (!Array.isArray(message.events))
                    return "events: array expected";
                for (let i = 0; i < message.events.length; ++i) {
                    let error = $root.epoch_proto.TimelineEvent.verify(message.events[i]);
                    if (error)
                        return "events." + error;
                }
            }
            return null;
        };

        /**
         * Creates a TimelineDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.TimelineDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.TimelineDef} TimelineDef
         */
        TimelineDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.TimelineDef)
                return object;
            let message = new $root.epoch_proto.TimelineDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.TimelineDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.events) {
                if (!Array.isArray(object.events))
                    throw TypeError(".epoch_proto.TimelineDef.events: array expected");
                message.events = [];
                for (let i = 0; i < object.events.length; ++i) {
                    if (typeof object.events[i] !== "object")
                        throw TypeError(".epoch_proto.TimelineDef.events: object expected");
                    message.events[i] = $root.epoch_proto.TimelineEvent.fromObject(object.events[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a TimelineDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.TimelineDef
         * @static
         * @param {epoch_proto.TimelineDef} message TimelineDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        TimelineDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.events = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.events && message.events.length) {
                object.events = [];
                for (let j = 0; j < message.events.length; ++j)
                    object.events[j] = $root.epoch_proto.TimelineEvent.toObject(message.events[j], options);
            }
            return object;
        };

        /**
         * Converts this TimelineDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.TimelineDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        TimelineDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for TimelineDef
         * @function getTypeUrl
         * @memberof epoch_proto.TimelineDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        TimelineDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.TimelineDef";
        };

        return TimelineDef;
    })();

    epoch_proto.ErrorBarPoint = (function() {

        /**
         * Properties of an ErrorBarPoint.
         * @memberof epoch_proto
         * @interface IErrorBarPoint
         * @property {number|Long|null} [x] ErrorBarPoint x
         * @property {number|null} [low] ErrorBarPoint low
         * @property {number|null} [high] ErrorBarPoint high
         */

        /**
         * Constructs a new ErrorBarPoint.
         * @memberof epoch_proto
         * @classdesc Represents an ErrorBarPoint.
         * @implements IErrorBarPoint
         * @constructor
         * @param {epoch_proto.IErrorBarPoint=} [properties] Properties to set
         */
        function ErrorBarPoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ErrorBarPoint x.
         * @member {number|Long} x
         * @memberof epoch_proto.ErrorBarPoint
         * @instance
         */
        ErrorBarPoint.prototype.x = $util.Long ? $util.Long.fromBits(0,0,false) : 0;

        /**
         * ErrorBarPoint low.
         * @member {number} low
         * @memberof epoch_proto.ErrorBarPoint
         * @instance
         */
        ErrorBarPoint.prototype.low = 0;

        /**
         * ErrorBarPoint high.
         * @member {number} high
         * @memberof epoch_proto.ErrorBarPoint
         * @instance
         */
        ErrorBarPoint.prototype.high = 0;

        /**
         * Creates a new ErrorBarPoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.ErrorBarPoint
         * @static
         * @param {epoch_proto.IErrorBarPoint=} [properties] Properties to set
         * @returns {epoch_proto.ErrorBarPoint} ErrorBarPoint instance
         */
        ErrorBarPoint.create = function create(properties) {
            return new ErrorBarPoint(properties);
        };

        /**
         * Encodes the specified ErrorBarPoint message. Does not implicitly {@link epoch_proto.ErrorBarPoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.ErrorBarPoint
         * @static
         * @param {epoch_proto.IErrorBarPoint} message ErrorBarPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ErrorBarPoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 0 =*/8).int64(message.x);
            if (message.low != null && Object.hasOwnProperty.call(message, "low"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.low);
            if (message.high != null && Object.hasOwnProperty.call(message, "high"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.high);
            return writer;
        };

        /**
         * Encodes the specified ErrorBarPoint message, length delimited. Does not implicitly {@link epoch_proto.ErrorBarPoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.ErrorBarPoint
         * @static
         * @param {epoch_proto.IErrorBarPoint} message ErrorBarPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ErrorBarPoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an ErrorBarPoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.ErrorBarPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.ErrorBarPoint} ErrorBarPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ErrorBarPoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.ErrorBarPoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.int64();
                        break;
                    }
                case 2: {
                        message.low = reader.double();
                        break;
                    }
                case 3: {
                        message.high = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an ErrorBarPoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.ErrorBarPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.ErrorBarPoint} ErrorBarPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ErrorBarPoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an ErrorBarPoint message.
         * @function verify
         * @memberof epoch_proto.ErrorBarPoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ErrorBarPoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.x != null && message.hasOwnProperty("x"))
                if (!$util.isInteger(message.x) && !(message.x && $util.isInteger(message.x.low) && $util.isInteger(message.x.high)))
                    return "x: integer|Long expected";
            if (message.low != null && message.hasOwnProperty("low"))
                if (typeof message.low !== "number")
                    return "low: number expected";
            if (message.high != null && message.hasOwnProperty("high"))
                if (typeof message.high !== "number")
                    return "high: number expected";
            return null;
        };

        /**
         * Creates an ErrorBarPoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.ErrorBarPoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.ErrorBarPoint} ErrorBarPoint
         */
        ErrorBarPoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.ErrorBarPoint)
                return object;
            let message = new $root.epoch_proto.ErrorBarPoint();
            if (object.x != null)
                if ($util.Long)
                    (message.x = $util.Long.fromValue(object.x)).unsigned = false;
                else if (typeof object.x === "string")
                    message.x = parseInt(object.x, 10);
                else if (typeof object.x === "number")
                    message.x = object.x;
                else if (typeof object.x === "object")
                    message.x = new $util.LongBits(object.x.low >>> 0, object.x.high >>> 0).toNumber();
            if (object.low != null)
                message.low = Number(object.low);
            if (object.high != null)
                message.high = Number(object.high);
            return message;
        };

        /**
         * Creates a plain object from an ErrorBarPoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.ErrorBarPoint
         * @static
         * @param {epoch_proto.ErrorBarPoint} message ErrorBarPoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ErrorBarPoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                if ($util.Long) {
                    let long = new $util.Long(0, 0, false);
                    object.x = options.longs === String ? long.toString() : options.longs === Number ? long.toNumber() : long;
                } else
                    object.x = options.longs === String ? "0" : 0;
                object.low = 0;
                object.high = 0;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x === "number")
                    object.x = options.longs === String ? String(message.x) : message.x;
                else
                    object.x = options.longs === String ? $util.Long.prototype.toString.call(message.x) : options.longs === Number ? new $util.LongBits(message.x.low >>> 0, message.x.high >>> 0).toNumber() : message.x;
            if (message.low != null && message.hasOwnProperty("low"))
                object.low = options.json && !isFinite(message.low) ? String(message.low) : message.low;
            if (message.high != null && message.hasOwnProperty("high"))
                object.high = options.json && !isFinite(message.high) ? String(message.high) : message.high;
            return object;
        };

        /**
         * Converts this ErrorBarPoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.ErrorBarPoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ErrorBarPoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ErrorBarPoint
         * @function getTypeUrl
         * @memberof epoch_proto.ErrorBarPoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ErrorBarPoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.ErrorBarPoint";
        };

        return ErrorBarPoint;
    })();

    epoch_proto.NumericErrorBarPoint = (function() {

        /**
         * Properties of a NumericErrorBarPoint.
         * @memberof epoch_proto
         * @interface INumericErrorBarPoint
         * @property {number|null} [x] NumericErrorBarPoint x
         * @property {number|null} [low] NumericErrorBarPoint low
         * @property {number|null} [high] NumericErrorBarPoint high
         */

        /**
         * Constructs a new NumericErrorBarPoint.
         * @memberof epoch_proto
         * @classdesc Represents a NumericErrorBarPoint.
         * @implements INumericErrorBarPoint
         * @constructor
         * @param {epoch_proto.INumericErrorBarPoint=} [properties] Properties to set
         */
        function NumericErrorBarPoint(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NumericErrorBarPoint x.
         * @member {number} x
         * @memberof epoch_proto.NumericErrorBarPoint
         * @instance
         */
        NumericErrorBarPoint.prototype.x = 0;

        /**
         * NumericErrorBarPoint low.
         * @member {number} low
         * @memberof epoch_proto.NumericErrorBarPoint
         * @instance
         */
        NumericErrorBarPoint.prototype.low = 0;

        /**
         * NumericErrorBarPoint high.
         * @member {number} high
         * @memberof epoch_proto.NumericErrorBarPoint
         * @instance
         */
        NumericErrorBarPoint.prototype.high = 0;

        /**
         * Creates a new NumericErrorBarPoint instance using the specified properties.
         * @function create
         * @memberof epoch_proto.NumericErrorBarPoint
         * @static
         * @param {epoch_proto.INumericErrorBarPoint=} [properties] Properties to set
         * @returns {epoch_proto.NumericErrorBarPoint} NumericErrorBarPoint instance
         */
        NumericErrorBarPoint.create = function create(properties) {
            return new NumericErrorBarPoint(properties);
        };

        /**
         * Encodes the specified NumericErrorBarPoint message. Does not implicitly {@link epoch_proto.NumericErrorBarPoint.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.NumericErrorBarPoint
         * @static
         * @param {epoch_proto.INumericErrorBarPoint} message NumericErrorBarPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericErrorBarPoint.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.x != null && Object.hasOwnProperty.call(message, "x"))
                writer.uint32(/* id 1, wireType 1 =*/9).double(message.x);
            if (message.low != null && Object.hasOwnProperty.call(message, "low"))
                writer.uint32(/* id 2, wireType 1 =*/17).double(message.low);
            if (message.high != null && Object.hasOwnProperty.call(message, "high"))
                writer.uint32(/* id 3, wireType 1 =*/25).double(message.high);
            return writer;
        };

        /**
         * Encodes the specified NumericErrorBarPoint message, length delimited. Does not implicitly {@link epoch_proto.NumericErrorBarPoint.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.NumericErrorBarPoint
         * @static
         * @param {epoch_proto.INumericErrorBarPoint} message NumericErrorBarPoint message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericErrorBarPoint.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NumericErrorBarPoint message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.NumericErrorBarPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.NumericErrorBarPoint} NumericErrorBarPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericErrorBarPoint.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.NumericErrorBarPoint();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.x = reader.double();
                        break;
                    }
                case 2: {
                        message.low = reader.double();
                        break;
                    }
                case 3: {
                        message.high = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NumericErrorBarPoint message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.NumericErrorBarPoint
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.NumericErrorBarPoint} NumericErrorBarPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericErrorBarPoint.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NumericErrorBarPoint message.
         * @function verify
         * @memberof epoch_proto.NumericErrorBarPoint
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NumericErrorBarPoint.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.x != null && message.hasOwnProperty("x"))
                if (typeof message.x !== "number")
                    return "x: number expected";
            if (message.low != null && message.hasOwnProperty("low"))
                if (typeof message.low !== "number")
                    return "low: number expected";
            if (message.high != null && message.hasOwnProperty("high"))
                if (typeof message.high !== "number")
                    return "high: number expected";
            return null;
        };

        /**
         * Creates a NumericErrorBarPoint message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.NumericErrorBarPoint
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.NumericErrorBarPoint} NumericErrorBarPoint
         */
        NumericErrorBarPoint.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.NumericErrorBarPoint)
                return object;
            let message = new $root.epoch_proto.NumericErrorBarPoint();
            if (object.x != null)
                message.x = Number(object.x);
            if (object.low != null)
                message.low = Number(object.low);
            if (object.high != null)
                message.high = Number(object.high);
            return message;
        };

        /**
         * Creates a plain object from a NumericErrorBarPoint message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.NumericErrorBarPoint
         * @static
         * @param {epoch_proto.NumericErrorBarPoint} message NumericErrorBarPoint
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NumericErrorBarPoint.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.x = 0;
                object.low = 0;
                object.high = 0;
            }
            if (message.x != null && message.hasOwnProperty("x"))
                object.x = options.json && !isFinite(message.x) ? String(message.x) : message.x;
            if (message.low != null && message.hasOwnProperty("low"))
                object.low = options.json && !isFinite(message.low) ? String(message.low) : message.low;
            if (message.high != null && message.hasOwnProperty("high"))
                object.high = options.json && !isFinite(message.high) ? String(message.high) : message.high;
            return object;
        };

        /**
         * Converts this NumericErrorBarPoint to JSON.
         * @function toJSON
         * @memberof epoch_proto.NumericErrorBarPoint
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NumericErrorBarPoint.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NumericErrorBarPoint
         * @function getTypeUrl
         * @memberof epoch_proto.NumericErrorBarPoint
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NumericErrorBarPoint.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.NumericErrorBarPoint";
        };

        return NumericErrorBarPoint;
    })();

    epoch_proto.ErrorBarSeries = (function() {

        /**
         * Properties of an ErrorBarSeries.
         * @memberof epoch_proto
         * @interface IErrorBarSeries
         * @property {string|null} [name] ErrorBarSeries name
         * @property {Array.<epoch_proto.IErrorBarPoint>|null} [data] ErrorBarSeries data
         * @property {string|null} [whiskerColor] ErrorBarSeries whiskerColor
         * @property {number|null} [whiskerWidth] ErrorBarSeries whiskerWidth
         */

        /**
         * Constructs a new ErrorBarSeries.
         * @memberof epoch_proto
         * @classdesc Represents an ErrorBarSeries.
         * @implements IErrorBarSeries
         * @constructor
         * @param {epoch_proto.IErrorBarSeries=} [properties] Properties to set
         */
        function ErrorBarSeries(properties) {
            this.data = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ErrorBarSeries name.
         * @member {string} name
         * @memberof epoch_proto.ErrorBarSeries
         * @instance
         */
        ErrorBarSeries.prototype.name = "";

        /**
         * ErrorBarSeries data.
         * @member {Array.<epoch_proto.IErrorBarPoint>} data
         * @memberof epoch_proto.ErrorBarSeries
         * @instance
         */
        ErrorBarSeries.prototype.data = $util.emptyArray;

        /**
         * ErrorBarSeries whiskerColor.
         * @member {string|null|undefined} whiskerColor
         * @memberof epoch_proto.ErrorBarSeries
         * @instance
         */
        ErrorBarSeries.prototype.whiskerColor = null;

        /**
         * ErrorBarSeries whiskerWidth.
         * @member {number|null|undefined} whiskerWidth
         * @memberof epoch_proto.ErrorBarSeries
         * @instance
         */
        ErrorBarSeries.prototype.whiskerWidth = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(ErrorBarSeries.prototype, "_whiskerColor", {
            get: $util.oneOfGetter($oneOfFields = ["whiskerColor"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(ErrorBarSeries.prototype, "_whiskerWidth", {
            get: $util.oneOfGetter($oneOfFields = ["whiskerWidth"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new ErrorBarSeries instance using the specified properties.
         * @function create
         * @memberof epoch_proto.ErrorBarSeries
         * @static
         * @param {epoch_proto.IErrorBarSeries=} [properties] Properties to set
         * @returns {epoch_proto.ErrorBarSeries} ErrorBarSeries instance
         */
        ErrorBarSeries.create = function create(properties) {
            return new ErrorBarSeries(properties);
        };

        /**
         * Encodes the specified ErrorBarSeries message. Does not implicitly {@link epoch_proto.ErrorBarSeries.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.ErrorBarSeries
         * @static
         * @param {epoch_proto.IErrorBarSeries} message ErrorBarSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ErrorBarSeries.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.name);
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.ErrorBarPoint.encode(message.data[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.whiskerColor != null && Object.hasOwnProperty.call(message, "whiskerColor"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.whiskerColor);
            if (message.whiskerWidth != null && Object.hasOwnProperty.call(message, "whiskerWidth"))
                writer.uint32(/* id 4, wireType 0 =*/32).uint32(message.whiskerWidth);
            return writer;
        };

        /**
         * Encodes the specified ErrorBarSeries message, length delimited. Does not implicitly {@link epoch_proto.ErrorBarSeries.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.ErrorBarSeries
         * @static
         * @param {epoch_proto.IErrorBarSeries} message ErrorBarSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ErrorBarSeries.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an ErrorBarSeries message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.ErrorBarSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.ErrorBarSeries} ErrorBarSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ErrorBarSeries.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.ErrorBarSeries();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.name = reader.string();
                        break;
                    }
                case 2: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.ErrorBarPoint.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.whiskerColor = reader.string();
                        break;
                    }
                case 4: {
                        message.whiskerWidth = reader.uint32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an ErrorBarSeries message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.ErrorBarSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.ErrorBarSeries} ErrorBarSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ErrorBarSeries.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an ErrorBarSeries message.
         * @function verify
         * @memberof epoch_proto.ErrorBarSeries
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ErrorBarSeries.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.ErrorBarPoint.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            if (message.whiskerColor != null && message.hasOwnProperty("whiskerColor")) {
                properties._whiskerColor = 1;
                if (!$util.isString(message.whiskerColor))
                    return "whiskerColor: string expected";
            }
            if (message.whiskerWidth != null && message.hasOwnProperty("whiskerWidth")) {
                properties._whiskerWidth = 1;
                if (!$util.isInteger(message.whiskerWidth))
                    return "whiskerWidth: integer expected";
            }
            return null;
        };

        /**
         * Creates an ErrorBarSeries message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.ErrorBarSeries
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.ErrorBarSeries} ErrorBarSeries
         */
        ErrorBarSeries.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.ErrorBarSeries)
                return object;
            let message = new $root.epoch_proto.ErrorBarSeries();
            if (object.name != null)
                message.name = String(object.name);
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.ErrorBarSeries.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.ErrorBarSeries.data: object expected");
                    message.data[i] = $root.epoch_proto.ErrorBarPoint.fromObject(object.data[i]);
                }
            }
            if (object.whiskerColor != null)
                message.whiskerColor = String(object.whiskerColor);
            if (object.whiskerWidth != null)
                message.whiskerWidth = object.whiskerWidth >>> 0;
            return message;
        };

        /**
         * Creates a plain object from an ErrorBarSeries message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.ErrorBarSeries
         * @static
         * @param {epoch_proto.ErrorBarSeries} message ErrorBarSeries
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ErrorBarSeries.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.data = [];
            if (options.defaults)
                object.name = "";
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.ErrorBarPoint.toObject(message.data[j], options);
            }
            if (message.whiskerColor != null && message.hasOwnProperty("whiskerColor")) {
                object.whiskerColor = message.whiskerColor;
                if (options.oneofs)
                    object._whiskerColor = "whiskerColor";
            }
            if (message.whiskerWidth != null && message.hasOwnProperty("whiskerWidth")) {
                object.whiskerWidth = message.whiskerWidth;
                if (options.oneofs)
                    object._whiskerWidth = "whiskerWidth";
            }
            return object;
        };

        /**
         * Converts this ErrorBarSeries to JSON.
         * @function toJSON
         * @memberof epoch_proto.ErrorBarSeries
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ErrorBarSeries.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ErrorBarSeries
         * @function getTypeUrl
         * @memberof epoch_proto.ErrorBarSeries
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ErrorBarSeries.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.ErrorBarSeries";
        };

        return ErrorBarSeries;
    })();

    epoch_proto.NumericErrorBarSeries = (function() {

        /**
         * Properties of a NumericErrorBarSeries.
         * @memberof epoch_proto
         * @interface INumericErrorBarSeries
         * @property {string|null} [name] NumericErrorBarSeries name
         * @property {Array.<epoch_proto.INumericErrorBarPoint>|null} [data] NumericErrorBarSeries data
         * @property {string|null} [whiskerColor] NumericErrorBarSeries whiskerColor
         * @property {number|null} [whiskerWidth] NumericErrorBarSeries whiskerWidth
         */

        /**
         * Constructs a new NumericErrorBarSeries.
         * @memberof epoch_proto
         * @classdesc Represents a NumericErrorBarSeries.
         * @implements INumericErrorBarSeries
         * @constructor
         * @param {epoch_proto.INumericErrorBarSeries=} [properties] Properties to set
         */
        function NumericErrorBarSeries(properties) {
            this.data = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NumericErrorBarSeries name.
         * @member {string} name
         * @memberof epoch_proto.NumericErrorBarSeries
         * @instance
         */
        NumericErrorBarSeries.prototype.name = "";

        /**
         * NumericErrorBarSeries data.
         * @member {Array.<epoch_proto.INumericErrorBarPoint>} data
         * @memberof epoch_proto.NumericErrorBarSeries
         * @instance
         */
        NumericErrorBarSeries.prototype.data = $util.emptyArray;

        /**
         * NumericErrorBarSeries whiskerColor.
         * @member {string|null|undefined} whiskerColor
         * @memberof epoch_proto.NumericErrorBarSeries
         * @instance
         */
        NumericErrorBarSeries.prototype.whiskerColor = null;

        /**
         * NumericErrorBarSeries whiskerWidth.
         * @member {number|null|undefined} whiskerWidth
         * @memberof epoch_proto.NumericErrorBarSeries
         * @instance
         */
        NumericErrorBarSeries.prototype.whiskerWidth = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(NumericErrorBarSeries.prototype, "_whiskerColor", {
            get: $util.oneOfGetter($oneOfFields = ["whiskerColor"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(NumericErrorBarSeries.prototype, "_whiskerWidth", {
            get: $util.oneOfGetter($oneOfFields = ["whiskerWidth"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new NumericErrorBarSeries instance using the specified properties.
         * @function create
         * @memberof epoch_proto.NumericErrorBarSeries
         * @static
         * @param {epoch_proto.INumericErrorBarSeries=} [properties] Properties to set
         * @returns {epoch_proto.NumericErrorBarSeries} NumericErrorBarSeries instance
         */
        NumericErrorBarSeries.create = function create(properties) {
            return new NumericErrorBarSeries(properties);
        };

        /**
         * Encodes the specified NumericErrorBarSeries message. Does not implicitly {@link epoch_proto.NumericErrorBarSeries.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.NumericErrorBarSeries
         * @static
         * @param {epoch_proto.INumericErrorBarSeries} message NumericErrorBarSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericErrorBarSeries.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.name != null && Object.hasOwnProperty.call(message, "name"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.name);
            if (message.data != null && message.data.length)
                for (let i = 0; i < message.data.length; ++i)
                    $root.epoch_proto.NumericErrorBarPoint.encode(message.data[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.whiskerColor != null && Object.hasOwnProperty.call(message, "whiskerColor"))
                writer.uint32(/* id 3, wireType 2 =*/26).string(message.whiskerColor);
            if (message.whiskerWidth != null && Object.hasOwnProperty.call(message, "whiskerWidth"))
                writer.uint32(/* id 4, wireType 0 =*/32).uint32(message.whiskerWidth);
            return writer;
        };

        /**
         * Encodes the specified NumericErrorBarSeries message, length delimited. Does not implicitly {@link epoch_proto.NumericErrorBarSeries.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.NumericErrorBarSeries
         * @static
         * @param {epoch_proto.INumericErrorBarSeries} message NumericErrorBarSeries message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericErrorBarSeries.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NumericErrorBarSeries message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.NumericErrorBarSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.NumericErrorBarSeries} NumericErrorBarSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericErrorBarSeries.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.NumericErrorBarSeries();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.name = reader.string();
                        break;
                    }
                case 2: {
                        if (!(message.data && message.data.length))
                            message.data = [];
                        message.data.push($root.epoch_proto.NumericErrorBarPoint.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.whiskerColor = reader.string();
                        break;
                    }
                case 4: {
                        message.whiskerWidth = reader.uint32();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NumericErrorBarSeries message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.NumericErrorBarSeries
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.NumericErrorBarSeries} NumericErrorBarSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericErrorBarSeries.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NumericErrorBarSeries message.
         * @function verify
         * @memberof epoch_proto.NumericErrorBarSeries
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NumericErrorBarSeries.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.name != null && message.hasOwnProperty("name"))
                if (!$util.isString(message.name))
                    return "name: string expected";
            if (message.data != null && message.hasOwnProperty("data")) {
                if (!Array.isArray(message.data))
                    return "data: array expected";
                for (let i = 0; i < message.data.length; ++i) {
                    let error = $root.epoch_proto.NumericErrorBarPoint.verify(message.data[i]);
                    if (error)
                        return "data." + error;
                }
            }
            if (message.whiskerColor != null && message.hasOwnProperty("whiskerColor")) {
                properties._whiskerColor = 1;
                if (!$util.isString(message.whiskerColor))
                    return "whiskerColor: string expected";
            }
            if (message.whiskerWidth != null && message.hasOwnProperty("whiskerWidth")) {
                properties._whiskerWidth = 1;
                if (!$util.isInteger(message.whiskerWidth))
                    return "whiskerWidth: integer expected";
            }
            return null;
        };

        /**
         * Creates a NumericErrorBarSeries message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.NumericErrorBarSeries
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.NumericErrorBarSeries} NumericErrorBarSeries
         */
        NumericErrorBarSeries.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.NumericErrorBarSeries)
                return object;
            let message = new $root.epoch_proto.NumericErrorBarSeries();
            if (object.name != null)
                message.name = String(object.name);
            if (object.data) {
                if (!Array.isArray(object.data))
                    throw TypeError(".epoch_proto.NumericErrorBarSeries.data: array expected");
                message.data = [];
                for (let i = 0; i < object.data.length; ++i) {
                    if (typeof object.data[i] !== "object")
                        throw TypeError(".epoch_proto.NumericErrorBarSeries.data: object expected");
                    message.data[i] = $root.epoch_proto.NumericErrorBarPoint.fromObject(object.data[i]);
                }
            }
            if (object.whiskerColor != null)
                message.whiskerColor = String(object.whiskerColor);
            if (object.whiskerWidth != null)
                message.whiskerWidth = object.whiskerWidth >>> 0;
            return message;
        };

        /**
         * Creates a plain object from a NumericErrorBarSeries message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.NumericErrorBarSeries
         * @static
         * @param {epoch_proto.NumericErrorBarSeries} message NumericErrorBarSeries
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NumericErrorBarSeries.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.data = [];
            if (options.defaults)
                object.name = "";
            if (message.name != null && message.hasOwnProperty("name"))
                object.name = message.name;
            if (message.data && message.data.length) {
                object.data = [];
                for (let j = 0; j < message.data.length; ++j)
                    object.data[j] = $root.epoch_proto.NumericErrorBarPoint.toObject(message.data[j], options);
            }
            if (message.whiskerColor != null && message.hasOwnProperty("whiskerColor")) {
                object.whiskerColor = message.whiskerColor;
                if (options.oneofs)
                    object._whiskerColor = "whiskerColor";
            }
            if (message.whiskerWidth != null && message.hasOwnProperty("whiskerWidth")) {
                object.whiskerWidth = message.whiskerWidth;
                if (options.oneofs)
                    object._whiskerWidth = "whiskerWidth";
            }
            return object;
        };

        /**
         * Converts this NumericErrorBarSeries to JSON.
         * @function toJSON
         * @memberof epoch_proto.NumericErrorBarSeries
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NumericErrorBarSeries.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NumericErrorBarSeries
         * @function getTypeUrl
         * @memberof epoch_proto.NumericErrorBarSeries
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NumericErrorBarSeries.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.NumericErrorBarSeries";
        };

        return NumericErrorBarSeries;
    })();

    epoch_proto.ErrorBarDef = (function() {

        /**
         * Properties of an ErrorBarDef.
         * @memberof epoch_proto
         * @interface IErrorBarDef
         * @property {epoch_proto.IChartDef|null} [chartDef] ErrorBarDef chartDef
         * @property {Array.<epoch_proto.IErrorBarSeries>|null} [series] ErrorBarDef series
         * @property {epoch_proto.ILine|null} [baseLine] ErrorBarDef baseLine
         */

        /**
         * Constructs a new ErrorBarDef.
         * @memberof epoch_proto
         * @classdesc Represents an ErrorBarDef.
         * @implements IErrorBarDef
         * @constructor
         * @param {epoch_proto.IErrorBarDef=} [properties] Properties to set
         */
        function ErrorBarDef(properties) {
            this.series = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ErrorBarDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.ErrorBarDef
         * @instance
         */
        ErrorBarDef.prototype.chartDef = null;

        /**
         * ErrorBarDef series.
         * @member {Array.<epoch_proto.IErrorBarSeries>} series
         * @memberof epoch_proto.ErrorBarDef
         * @instance
         */
        ErrorBarDef.prototype.series = $util.emptyArray;

        /**
         * ErrorBarDef baseLine.
         * @member {epoch_proto.ILine|null|undefined} baseLine
         * @memberof epoch_proto.ErrorBarDef
         * @instance
         */
        ErrorBarDef.prototype.baseLine = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(ErrorBarDef.prototype, "_baseLine", {
            get: $util.oneOfGetter($oneOfFields = ["baseLine"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new ErrorBarDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.ErrorBarDef
         * @static
         * @param {epoch_proto.IErrorBarDef=} [properties] Properties to set
         * @returns {epoch_proto.ErrorBarDef} ErrorBarDef instance
         */
        ErrorBarDef.create = function create(properties) {
            return new ErrorBarDef(properties);
        };

        /**
         * Encodes the specified ErrorBarDef message. Does not implicitly {@link epoch_proto.ErrorBarDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.ErrorBarDef
         * @static
         * @param {epoch_proto.IErrorBarDef} message ErrorBarDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ErrorBarDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.series != null && message.series.length)
                for (let i = 0; i < message.series.length; ++i)
                    $root.epoch_proto.ErrorBarSeries.encode(message.series[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.baseLine != null && Object.hasOwnProperty.call(message, "baseLine"))
                $root.epoch_proto.Line.encode(message.baseLine, writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ErrorBarDef message, length delimited. Does not implicitly {@link epoch_proto.ErrorBarDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.ErrorBarDef
         * @static
         * @param {epoch_proto.IErrorBarDef} message ErrorBarDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ErrorBarDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes an ErrorBarDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.ErrorBarDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.ErrorBarDef} ErrorBarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ErrorBarDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.ErrorBarDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.series && message.series.length))
                            message.series = [];
                        message.series.push($root.epoch_proto.ErrorBarSeries.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.baseLine = $root.epoch_proto.Line.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes an ErrorBarDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.ErrorBarDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.ErrorBarDef} ErrorBarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ErrorBarDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies an ErrorBarDef message.
         * @function verify
         * @memberof epoch_proto.ErrorBarDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ErrorBarDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.series != null && message.hasOwnProperty("series")) {
                if (!Array.isArray(message.series))
                    return "series: array expected";
                for (let i = 0; i < message.series.length; ++i) {
                    let error = $root.epoch_proto.ErrorBarSeries.verify(message.series[i]);
                    if (error)
                        return "series." + error;
                }
            }
            if (message.baseLine != null && message.hasOwnProperty("baseLine")) {
                properties._baseLine = 1;
                {
                    let error = $root.epoch_proto.Line.verify(message.baseLine);
                    if (error)
                        return "baseLine." + error;
                }
            }
            return null;
        };

        /**
         * Creates an ErrorBarDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.ErrorBarDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.ErrorBarDef} ErrorBarDef
         */
        ErrorBarDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.ErrorBarDef)
                return object;
            let message = new $root.epoch_proto.ErrorBarDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.ErrorBarDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.series) {
                if (!Array.isArray(object.series))
                    throw TypeError(".epoch_proto.ErrorBarDef.series: array expected");
                message.series = [];
                for (let i = 0; i < object.series.length; ++i) {
                    if (typeof object.series[i] !== "object")
                        throw TypeError(".epoch_proto.ErrorBarDef.series: object expected");
                    message.series[i] = $root.epoch_proto.ErrorBarSeries.fromObject(object.series[i]);
                }
            }
            if (object.baseLine != null) {
                if (typeof object.baseLine !== "object")
                    throw TypeError(".epoch_proto.ErrorBarDef.baseLine: object expected");
                message.baseLine = $root.epoch_proto.Line.fromObject(object.baseLine);
            }
            return message;
        };

        /**
         * Creates a plain object from an ErrorBarDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.ErrorBarDef
         * @static
         * @param {epoch_proto.ErrorBarDef} message ErrorBarDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ErrorBarDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.series = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.series && message.series.length) {
                object.series = [];
                for (let j = 0; j < message.series.length; ++j)
                    object.series[j] = $root.epoch_proto.ErrorBarSeries.toObject(message.series[j], options);
            }
            if (message.baseLine != null && message.hasOwnProperty("baseLine")) {
                object.baseLine = $root.epoch_proto.Line.toObject(message.baseLine, options);
                if (options.oneofs)
                    object._baseLine = "baseLine";
            }
            return object;
        };

        /**
         * Converts this ErrorBarDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.ErrorBarDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ErrorBarDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ErrorBarDef
         * @function getTypeUrl
         * @memberof epoch_proto.ErrorBarDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ErrorBarDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.ErrorBarDef";
        };

        return ErrorBarDef;
    })();

    epoch_proto.NumericErrorBarDef = (function() {

        /**
         * Properties of a NumericErrorBarDef.
         * @memberof epoch_proto
         * @interface INumericErrorBarDef
         * @property {epoch_proto.IChartDef|null} [chartDef] NumericErrorBarDef chartDef
         * @property {Array.<epoch_proto.INumericErrorBarSeries>|null} [series] NumericErrorBarDef series
         * @property {epoch_proto.INumericLine|null} [baseLine] NumericErrorBarDef baseLine
         */

        /**
         * Constructs a new NumericErrorBarDef.
         * @memberof epoch_proto
         * @classdesc Represents a NumericErrorBarDef.
         * @implements INumericErrorBarDef
         * @constructor
         * @param {epoch_proto.INumericErrorBarDef=} [properties] Properties to set
         */
        function NumericErrorBarDef(properties) {
            this.series = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * NumericErrorBarDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.NumericErrorBarDef
         * @instance
         */
        NumericErrorBarDef.prototype.chartDef = null;

        /**
         * NumericErrorBarDef series.
         * @member {Array.<epoch_proto.INumericErrorBarSeries>} series
         * @memberof epoch_proto.NumericErrorBarDef
         * @instance
         */
        NumericErrorBarDef.prototype.series = $util.emptyArray;

        /**
         * NumericErrorBarDef baseLine.
         * @member {epoch_proto.INumericLine|null|undefined} baseLine
         * @memberof epoch_proto.NumericErrorBarDef
         * @instance
         */
        NumericErrorBarDef.prototype.baseLine = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(NumericErrorBarDef.prototype, "_baseLine", {
            get: $util.oneOfGetter($oneOfFields = ["baseLine"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new NumericErrorBarDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.NumericErrorBarDef
         * @static
         * @param {epoch_proto.INumericErrorBarDef=} [properties] Properties to set
         * @returns {epoch_proto.NumericErrorBarDef} NumericErrorBarDef instance
         */
        NumericErrorBarDef.create = function create(properties) {
            return new NumericErrorBarDef(properties);
        };

        /**
         * Encodes the specified NumericErrorBarDef message. Does not implicitly {@link epoch_proto.NumericErrorBarDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.NumericErrorBarDef
         * @static
         * @param {epoch_proto.INumericErrorBarDef} message NumericErrorBarDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericErrorBarDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.series != null && message.series.length)
                for (let i = 0; i < message.series.length; ++i)
                    $root.epoch_proto.NumericErrorBarSeries.encode(message.series[i], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.baseLine != null && Object.hasOwnProperty.call(message, "baseLine"))
                $root.epoch_proto.NumericLine.encode(message.baseLine, writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified NumericErrorBarDef message, length delimited. Does not implicitly {@link epoch_proto.NumericErrorBarDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.NumericErrorBarDef
         * @static
         * @param {epoch_proto.INumericErrorBarDef} message NumericErrorBarDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        NumericErrorBarDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a NumericErrorBarDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.NumericErrorBarDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.NumericErrorBarDef} NumericErrorBarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericErrorBarDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.NumericErrorBarDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.series && message.series.length))
                            message.series = [];
                        message.series.push($root.epoch_proto.NumericErrorBarSeries.decode(reader, reader.uint32()));
                        break;
                    }
                case 3: {
                        message.baseLine = $root.epoch_proto.NumericLine.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a NumericErrorBarDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.NumericErrorBarDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.NumericErrorBarDef} NumericErrorBarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        NumericErrorBarDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a NumericErrorBarDef message.
         * @function verify
         * @memberof epoch_proto.NumericErrorBarDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        NumericErrorBarDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.series != null && message.hasOwnProperty("series")) {
                if (!Array.isArray(message.series))
                    return "series: array expected";
                for (let i = 0; i < message.series.length; ++i) {
                    let error = $root.epoch_proto.NumericErrorBarSeries.verify(message.series[i]);
                    if (error)
                        return "series." + error;
                }
            }
            if (message.baseLine != null && message.hasOwnProperty("baseLine")) {
                properties._baseLine = 1;
                {
                    let error = $root.epoch_proto.NumericLine.verify(message.baseLine);
                    if (error)
                        return "baseLine." + error;
                }
            }
            return null;
        };

        /**
         * Creates a NumericErrorBarDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.NumericErrorBarDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.NumericErrorBarDef} NumericErrorBarDef
         */
        NumericErrorBarDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.NumericErrorBarDef)
                return object;
            let message = new $root.epoch_proto.NumericErrorBarDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.NumericErrorBarDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.series) {
                if (!Array.isArray(object.series))
                    throw TypeError(".epoch_proto.NumericErrorBarDef.series: array expected");
                message.series = [];
                for (let i = 0; i < object.series.length; ++i) {
                    if (typeof object.series[i] !== "object")
                        throw TypeError(".epoch_proto.NumericErrorBarDef.series: object expected");
                    message.series[i] = $root.epoch_proto.NumericErrorBarSeries.fromObject(object.series[i]);
                }
            }
            if (object.baseLine != null) {
                if (typeof object.baseLine !== "object")
                    throw TypeError(".epoch_proto.NumericErrorBarDef.baseLine: object expected");
                message.baseLine = $root.epoch_proto.NumericLine.fromObject(object.baseLine);
            }
            return message;
        };

        /**
         * Creates a plain object from a NumericErrorBarDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.NumericErrorBarDef
         * @static
         * @param {epoch_proto.NumericErrorBarDef} message NumericErrorBarDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        NumericErrorBarDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.series = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.series && message.series.length) {
                object.series = [];
                for (let j = 0; j < message.series.length; ++j)
                    object.series[j] = $root.epoch_proto.NumericErrorBarSeries.toObject(message.series[j], options);
            }
            if (message.baseLine != null && message.hasOwnProperty("baseLine")) {
                object.baseLine = $root.epoch_proto.NumericLine.toObject(message.baseLine, options);
                if (options.oneofs)
                    object._baseLine = "baseLine";
            }
            return object;
        };

        /**
         * Converts this NumericErrorBarDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.NumericErrorBarDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        NumericErrorBarDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for NumericErrorBarDef
         * @function getTypeUrl
         * @memberof epoch_proto.NumericErrorBarDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        NumericErrorBarDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.NumericErrorBarDef";
        };

        return NumericErrorBarDef;
    })();

    epoch_proto.BellCurveDef = (function() {

        /**
         * Properties of a BellCurveDef.
         * @memberof epoch_proto
         * @interface IBellCurveDef
         * @property {epoch_proto.IChartDef|null} [chartDef] BellCurveDef chartDef
         * @property {Array.<number>|null} [baseData] BellCurveDef baseData
         * @property {number|null} [intervals] BellCurveDef intervals
         * @property {number|null} [pointsInInterval] BellCurveDef pointsInInterval
         * @property {string|null} [fillColor] BellCurveDef fillColor
         * @property {number|null} [fillOpacity] BellCurveDef fillOpacity
         */

        /**
         * Constructs a new BellCurveDef.
         * @memberof epoch_proto
         * @classdesc Represents a BellCurveDef.
         * @implements IBellCurveDef
         * @constructor
         * @param {epoch_proto.IBellCurveDef=} [properties] Properties to set
         */
        function BellCurveDef(properties) {
            this.baseData = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * BellCurveDef chartDef.
         * @member {epoch_proto.IChartDef|null|undefined} chartDef
         * @memberof epoch_proto.BellCurveDef
         * @instance
         */
        BellCurveDef.prototype.chartDef = null;

        /**
         * BellCurveDef baseData.
         * @member {Array.<number>} baseData
         * @memberof epoch_proto.BellCurveDef
         * @instance
         */
        BellCurveDef.prototype.baseData = $util.emptyArray;

        /**
         * BellCurveDef intervals.
         * @member {number|null|undefined} intervals
         * @memberof epoch_proto.BellCurveDef
         * @instance
         */
        BellCurveDef.prototype.intervals = null;

        /**
         * BellCurveDef pointsInInterval.
         * @member {number|null|undefined} pointsInInterval
         * @memberof epoch_proto.BellCurveDef
         * @instance
         */
        BellCurveDef.prototype.pointsInInterval = null;

        /**
         * BellCurveDef fillColor.
         * @member {string|null|undefined} fillColor
         * @memberof epoch_proto.BellCurveDef
         * @instance
         */
        BellCurveDef.prototype.fillColor = null;

        /**
         * BellCurveDef fillOpacity.
         * @member {number|null|undefined} fillOpacity
         * @memberof epoch_proto.BellCurveDef
         * @instance
         */
        BellCurveDef.prototype.fillOpacity = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BellCurveDef.prototype, "_intervals", {
            get: $util.oneOfGetter($oneOfFields = ["intervals"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BellCurveDef.prototype, "_pointsInInterval", {
            get: $util.oneOfGetter($oneOfFields = ["pointsInInterval"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BellCurveDef.prototype, "_fillColor", {
            get: $util.oneOfGetter($oneOfFields = ["fillColor"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        // Virtual OneOf for proto3 optional field
        Object.defineProperty(BellCurveDef.prototype, "_fillOpacity", {
            get: $util.oneOfGetter($oneOfFields = ["fillOpacity"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new BellCurveDef instance using the specified properties.
         * @function create
         * @memberof epoch_proto.BellCurveDef
         * @static
         * @param {epoch_proto.IBellCurveDef=} [properties] Properties to set
         * @returns {epoch_proto.BellCurveDef} BellCurveDef instance
         */
        BellCurveDef.create = function create(properties) {
            return new BellCurveDef(properties);
        };

        /**
         * Encodes the specified BellCurveDef message. Does not implicitly {@link epoch_proto.BellCurveDef.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.BellCurveDef
         * @static
         * @param {epoch_proto.IBellCurveDef} message BellCurveDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BellCurveDef.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.chartDef != null && Object.hasOwnProperty.call(message, "chartDef"))
                $root.epoch_proto.ChartDef.encode(message.chartDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.baseData != null && message.baseData.length) {
                writer.uint32(/* id 2, wireType 2 =*/18).fork();
                for (let i = 0; i < message.baseData.length; ++i)
                    writer.double(message.baseData[i]);
                writer.ldelim();
            }
            if (message.intervals != null && Object.hasOwnProperty.call(message, "intervals"))
                writer.uint32(/* id 3, wireType 0 =*/24).uint32(message.intervals);
            if (message.pointsInInterval != null && Object.hasOwnProperty.call(message, "pointsInInterval"))
                writer.uint32(/* id 4, wireType 0 =*/32).uint32(message.pointsInInterval);
            if (message.fillColor != null && Object.hasOwnProperty.call(message, "fillColor"))
                writer.uint32(/* id 5, wireType 2 =*/42).string(message.fillColor);
            if (message.fillOpacity != null && Object.hasOwnProperty.call(message, "fillOpacity"))
                writer.uint32(/* id 6, wireType 1 =*/49).double(message.fillOpacity);
            return writer;
        };

        /**
         * Encodes the specified BellCurveDef message, length delimited. Does not implicitly {@link epoch_proto.BellCurveDef.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.BellCurveDef
         * @static
         * @param {epoch_proto.IBellCurveDef} message BellCurveDef message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        BellCurveDef.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a BellCurveDef message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.BellCurveDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.BellCurveDef} BellCurveDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BellCurveDef.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.BellCurveDef();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.chartDef = $root.epoch_proto.ChartDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        if (!(message.baseData && message.baseData.length))
                            message.baseData = [];
                        if ((tag & 7) === 2) {
                            let end2 = reader.uint32() + reader.pos;
                            while (reader.pos < end2)
                                message.baseData.push(reader.double());
                        } else
                            message.baseData.push(reader.double());
                        break;
                    }
                case 3: {
                        message.intervals = reader.uint32();
                        break;
                    }
                case 4: {
                        message.pointsInInterval = reader.uint32();
                        break;
                    }
                case 5: {
                        message.fillColor = reader.string();
                        break;
                    }
                case 6: {
                        message.fillOpacity = reader.double();
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a BellCurveDef message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.BellCurveDef
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.BellCurveDef} BellCurveDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        BellCurveDef.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a BellCurveDef message.
         * @function verify
         * @memberof epoch_proto.BellCurveDef
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        BellCurveDef.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.chartDef != null && message.hasOwnProperty("chartDef")) {
                let error = $root.epoch_proto.ChartDef.verify(message.chartDef);
                if (error)
                    return "chartDef." + error;
            }
            if (message.baseData != null && message.hasOwnProperty("baseData")) {
                if (!Array.isArray(message.baseData))
                    return "baseData: array expected";
                for (let i = 0; i < message.baseData.length; ++i)
                    if (typeof message.baseData[i] !== "number")
                        return "baseData: number[] expected";
            }
            if (message.intervals != null && message.hasOwnProperty("intervals")) {
                properties._intervals = 1;
                if (!$util.isInteger(message.intervals))
                    return "intervals: integer expected";
            }
            if (message.pointsInInterval != null && message.hasOwnProperty("pointsInInterval")) {
                properties._pointsInInterval = 1;
                if (!$util.isInteger(message.pointsInInterval))
                    return "pointsInInterval: integer expected";
            }
            if (message.fillColor != null && message.hasOwnProperty("fillColor")) {
                properties._fillColor = 1;
                if (!$util.isString(message.fillColor))
                    return "fillColor: string expected";
            }
            if (message.fillOpacity != null && message.hasOwnProperty("fillOpacity")) {
                properties._fillOpacity = 1;
                if (typeof message.fillOpacity !== "number")
                    return "fillOpacity: number expected";
            }
            return null;
        };

        /**
         * Creates a BellCurveDef message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.BellCurveDef
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.BellCurveDef} BellCurveDef
         */
        BellCurveDef.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.BellCurveDef)
                return object;
            let message = new $root.epoch_proto.BellCurveDef();
            if (object.chartDef != null) {
                if (typeof object.chartDef !== "object")
                    throw TypeError(".epoch_proto.BellCurveDef.chartDef: object expected");
                message.chartDef = $root.epoch_proto.ChartDef.fromObject(object.chartDef);
            }
            if (object.baseData) {
                if (!Array.isArray(object.baseData))
                    throw TypeError(".epoch_proto.BellCurveDef.baseData: array expected");
                message.baseData = [];
                for (let i = 0; i < object.baseData.length; ++i)
                    message.baseData[i] = Number(object.baseData[i]);
            }
            if (object.intervals != null)
                message.intervals = object.intervals >>> 0;
            if (object.pointsInInterval != null)
                message.pointsInInterval = object.pointsInInterval >>> 0;
            if (object.fillColor != null)
                message.fillColor = String(object.fillColor);
            if (object.fillOpacity != null)
                message.fillOpacity = Number(object.fillOpacity);
            return message;
        };

        /**
         * Creates a plain object from a BellCurveDef message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.BellCurveDef
         * @static
         * @param {epoch_proto.BellCurveDef} message BellCurveDef
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        BellCurveDef.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.baseData = [];
            if (options.defaults)
                object.chartDef = null;
            if (message.chartDef != null && message.hasOwnProperty("chartDef"))
                object.chartDef = $root.epoch_proto.ChartDef.toObject(message.chartDef, options);
            if (message.baseData && message.baseData.length) {
                object.baseData = [];
                for (let j = 0; j < message.baseData.length; ++j)
                    object.baseData[j] = options.json && !isFinite(message.baseData[j]) ? String(message.baseData[j]) : message.baseData[j];
            }
            if (message.intervals != null && message.hasOwnProperty("intervals")) {
                object.intervals = message.intervals;
                if (options.oneofs)
                    object._intervals = "intervals";
            }
            if (message.pointsInInterval != null && message.hasOwnProperty("pointsInInterval")) {
                object.pointsInInterval = message.pointsInInterval;
                if (options.oneofs)
                    object._pointsInInterval = "pointsInInterval";
            }
            if (message.fillColor != null && message.hasOwnProperty("fillColor")) {
                object.fillColor = message.fillColor;
                if (options.oneofs)
                    object._fillColor = "fillColor";
            }
            if (message.fillOpacity != null && message.hasOwnProperty("fillOpacity")) {
                object.fillOpacity = options.json && !isFinite(message.fillOpacity) ? String(message.fillOpacity) : message.fillOpacity;
                if (options.oneofs)
                    object._fillOpacity = "fillOpacity";
            }
            return object;
        };

        /**
         * Converts this BellCurveDef to JSON.
         * @function toJSON
         * @memberof epoch_proto.BellCurveDef
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        BellCurveDef.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for BellCurveDef
         * @function getTypeUrl
         * @memberof epoch_proto.BellCurveDef
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        BellCurveDef.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.BellCurveDef";
        };

        return BellCurveDef;
    })();

    epoch_proto.Chart = (function() {

        /**
         * Properties of a Chart.
         * @memberof epoch_proto
         * @interface IChart
         * @property {epoch_proto.ILinesDef|null} [linesDef] Chart linesDef
         * @property {epoch_proto.IHeatMapDef|null} [heatMapDef] Chart heatMapDef
         * @property {epoch_proto.IBarDef|null} [barDef] Chart barDef
         * @property {epoch_proto.IHistogramDef|null} [histogramDef] Chart histogramDef
         * @property {epoch_proto.IBoxPlotDef|null} [boxPlotDef] Chart boxPlotDef
         * @property {epoch_proto.IXRangeDef|null} [xRangeDef] Chart xRangeDef
         * @property {epoch_proto.IPieDef|null} [pieDef] Chart pieDef
         * @property {epoch_proto.IAreaDef|null} [areaDef] Chart areaDef
         * @property {epoch_proto.INumericLinesDef|null} [numericLinesDef] Chart numericLinesDef
         * @property {epoch_proto.IScatterDef|null} [scatterDef] Chart scatterDef
         * @property {epoch_proto.IWaterfallDef|null} [waterfallDef] Chart waterfallDef
         * @property {epoch_proto.ISplineDef|null} [splineDef] Chart splineDef
         * @property {epoch_proto.INumericSplineDef|null} [numericSplineDef] Chart numericSplineDef
         * @property {epoch_proto.IBubbleDef|null} [bubbleDef] Chart bubbleDef
         * @property {epoch_proto.ITreemapDef|null} [treemapDef] Chart treemapDef
         * @property {epoch_proto.ISankeyDef|null} [sankeyDef] Chart sankeyDef
         * @property {epoch_proto.IAreaRangeDef|null} [areaRangeDef] Chart areaRangeDef
         * @property {epoch_proto.IGaugeDef|null} [gaugeDef] Chart gaugeDef
         * @property {epoch_proto.IBulletDef|null} [bulletDef] Chart bulletDef
         * @property {epoch_proto.ITimelineDef|null} [timelineDef] Chart timelineDef
         * @property {epoch_proto.IErrorBarDef|null} [errorBarDef] Chart errorBarDef
         * @property {epoch_proto.IBellCurveDef|null} [bellCurveDef] Chart bellCurveDef
         * @property {epoch_proto.INumericErrorBarDef|null} [numericErrorBarDef] Chart numericErrorBarDef
         */

        /**
         * Constructs a new Chart.
         * @memberof epoch_proto
         * @classdesc Represents a Chart.
         * @implements IChart
         * @constructor
         * @param {epoch_proto.IChart=} [properties] Properties to set
         */
        function Chart(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * Chart linesDef.
         * @member {epoch_proto.ILinesDef|null|undefined} linesDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.linesDef = null;

        /**
         * Chart heatMapDef.
         * @member {epoch_proto.IHeatMapDef|null|undefined} heatMapDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.heatMapDef = null;

        /**
         * Chart barDef.
         * @member {epoch_proto.IBarDef|null|undefined} barDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.barDef = null;

        /**
         * Chart histogramDef.
         * @member {epoch_proto.IHistogramDef|null|undefined} histogramDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.histogramDef = null;

        /**
         * Chart boxPlotDef.
         * @member {epoch_proto.IBoxPlotDef|null|undefined} boxPlotDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.boxPlotDef = null;

        /**
         * Chart xRangeDef.
         * @member {epoch_proto.IXRangeDef|null|undefined} xRangeDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.xRangeDef = null;

        /**
         * Chart pieDef.
         * @member {epoch_proto.IPieDef|null|undefined} pieDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.pieDef = null;

        /**
         * Chart areaDef.
         * @member {epoch_proto.IAreaDef|null|undefined} areaDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.areaDef = null;

        /**
         * Chart numericLinesDef.
         * @member {epoch_proto.INumericLinesDef|null|undefined} numericLinesDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.numericLinesDef = null;

        /**
         * Chart scatterDef.
         * @member {epoch_proto.IScatterDef|null|undefined} scatterDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.scatterDef = null;

        /**
         * Chart waterfallDef.
         * @member {epoch_proto.IWaterfallDef|null|undefined} waterfallDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.waterfallDef = null;

        /**
         * Chart splineDef.
         * @member {epoch_proto.ISplineDef|null|undefined} splineDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.splineDef = null;

        /**
         * Chart numericSplineDef.
         * @member {epoch_proto.INumericSplineDef|null|undefined} numericSplineDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.numericSplineDef = null;

        /**
         * Chart bubbleDef.
         * @member {epoch_proto.IBubbleDef|null|undefined} bubbleDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.bubbleDef = null;

        /**
         * Chart treemapDef.
         * @member {epoch_proto.ITreemapDef|null|undefined} treemapDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.treemapDef = null;

        /**
         * Chart sankeyDef.
         * @member {epoch_proto.ISankeyDef|null|undefined} sankeyDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.sankeyDef = null;

        /**
         * Chart areaRangeDef.
         * @member {epoch_proto.IAreaRangeDef|null|undefined} areaRangeDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.areaRangeDef = null;

        /**
         * Chart gaugeDef.
         * @member {epoch_proto.IGaugeDef|null|undefined} gaugeDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.gaugeDef = null;

        /**
         * Chart bulletDef.
         * @member {epoch_proto.IBulletDef|null|undefined} bulletDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.bulletDef = null;

        /**
         * Chart timelineDef.
         * @member {epoch_proto.ITimelineDef|null|undefined} timelineDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.timelineDef = null;

        /**
         * Chart errorBarDef.
         * @member {epoch_proto.IErrorBarDef|null|undefined} errorBarDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.errorBarDef = null;

        /**
         * Chart bellCurveDef.
         * @member {epoch_proto.IBellCurveDef|null|undefined} bellCurveDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.bellCurveDef = null;

        /**
         * Chart numericErrorBarDef.
         * @member {epoch_proto.INumericErrorBarDef|null|undefined} numericErrorBarDef
         * @memberof epoch_proto.Chart
         * @instance
         */
        Chart.prototype.numericErrorBarDef = null;

        // OneOf field names bound to virtual getters and setters
        let $oneOfFields;

        /**
         * Chart chartType.
         * @member {"linesDef"|"heatMapDef"|"barDef"|"histogramDef"|"boxPlotDef"|"xRangeDef"|"pieDef"|"areaDef"|"numericLinesDef"|"scatterDef"|"waterfallDef"|"splineDef"|"numericSplineDef"|"bubbleDef"|"treemapDef"|"sankeyDef"|"areaRangeDef"|"gaugeDef"|"bulletDef"|"timelineDef"|"errorBarDef"|"bellCurveDef"|"numericErrorBarDef"|undefined} chartType
         * @memberof epoch_proto.Chart
         * @instance
         */
        Object.defineProperty(Chart.prototype, "chartType", {
            get: $util.oneOfGetter($oneOfFields = ["linesDef", "heatMapDef", "barDef", "histogramDef", "boxPlotDef", "xRangeDef", "pieDef", "areaDef", "numericLinesDef", "scatterDef", "waterfallDef", "splineDef", "numericSplineDef", "bubbleDef", "treemapDef", "sankeyDef", "areaRangeDef", "gaugeDef", "bulletDef", "timelineDef", "errorBarDef", "bellCurveDef", "numericErrorBarDef"]),
            set: $util.oneOfSetter($oneOfFields)
        });

        /**
         * Creates a new Chart instance using the specified properties.
         * @function create
         * @memberof epoch_proto.Chart
         * @static
         * @param {epoch_proto.IChart=} [properties] Properties to set
         * @returns {epoch_proto.Chart} Chart instance
         */
        Chart.create = function create(properties) {
            return new Chart(properties);
        };

        /**
         * Encodes the specified Chart message. Does not implicitly {@link epoch_proto.Chart.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.Chart
         * @static
         * @param {epoch_proto.IChart} message Chart message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Chart.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.linesDef != null && Object.hasOwnProperty.call(message, "linesDef"))
                $root.epoch_proto.LinesDef.encode(message.linesDef, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.heatMapDef != null && Object.hasOwnProperty.call(message, "heatMapDef"))
                $root.epoch_proto.HeatMapDef.encode(message.heatMapDef, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.barDef != null && Object.hasOwnProperty.call(message, "barDef"))
                $root.epoch_proto.BarDef.encode(message.barDef, writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            if (message.histogramDef != null && Object.hasOwnProperty.call(message, "histogramDef"))
                $root.epoch_proto.HistogramDef.encode(message.histogramDef, writer.uint32(/* id 4, wireType 2 =*/34).fork()).ldelim();
            if (message.boxPlotDef != null && Object.hasOwnProperty.call(message, "boxPlotDef"))
                $root.epoch_proto.BoxPlotDef.encode(message.boxPlotDef, writer.uint32(/* id 5, wireType 2 =*/42).fork()).ldelim();
            if (message.xRangeDef != null && Object.hasOwnProperty.call(message, "xRangeDef"))
                $root.epoch_proto.XRangeDef.encode(message.xRangeDef, writer.uint32(/* id 6, wireType 2 =*/50).fork()).ldelim();
            if (message.pieDef != null && Object.hasOwnProperty.call(message, "pieDef"))
                $root.epoch_proto.PieDef.encode(message.pieDef, writer.uint32(/* id 7, wireType 2 =*/58).fork()).ldelim();
            if (message.areaDef != null && Object.hasOwnProperty.call(message, "areaDef"))
                $root.epoch_proto.AreaDef.encode(message.areaDef, writer.uint32(/* id 8, wireType 2 =*/66).fork()).ldelim();
            if (message.numericLinesDef != null && Object.hasOwnProperty.call(message, "numericLinesDef"))
                $root.epoch_proto.NumericLinesDef.encode(message.numericLinesDef, writer.uint32(/* id 9, wireType 2 =*/74).fork()).ldelim();
            if (message.scatterDef != null && Object.hasOwnProperty.call(message, "scatterDef"))
                $root.epoch_proto.ScatterDef.encode(message.scatterDef, writer.uint32(/* id 10, wireType 2 =*/82).fork()).ldelim();
            if (message.waterfallDef != null && Object.hasOwnProperty.call(message, "waterfallDef"))
                $root.epoch_proto.WaterfallDef.encode(message.waterfallDef, writer.uint32(/* id 11, wireType 2 =*/90).fork()).ldelim();
            if (message.splineDef != null && Object.hasOwnProperty.call(message, "splineDef"))
                $root.epoch_proto.SplineDef.encode(message.splineDef, writer.uint32(/* id 12, wireType 2 =*/98).fork()).ldelim();
            if (message.numericSplineDef != null && Object.hasOwnProperty.call(message, "numericSplineDef"))
                $root.epoch_proto.NumericSplineDef.encode(message.numericSplineDef, writer.uint32(/* id 13, wireType 2 =*/106).fork()).ldelim();
            if (message.bubbleDef != null && Object.hasOwnProperty.call(message, "bubbleDef"))
                $root.epoch_proto.BubbleDef.encode(message.bubbleDef, writer.uint32(/* id 14, wireType 2 =*/114).fork()).ldelim();
            if (message.treemapDef != null && Object.hasOwnProperty.call(message, "treemapDef"))
                $root.epoch_proto.TreemapDef.encode(message.treemapDef, writer.uint32(/* id 15, wireType 2 =*/122).fork()).ldelim();
            if (message.sankeyDef != null && Object.hasOwnProperty.call(message, "sankeyDef"))
                $root.epoch_proto.SankeyDef.encode(message.sankeyDef, writer.uint32(/* id 16, wireType 2 =*/130).fork()).ldelim();
            if (message.areaRangeDef != null && Object.hasOwnProperty.call(message, "areaRangeDef"))
                $root.epoch_proto.AreaRangeDef.encode(message.areaRangeDef, writer.uint32(/* id 17, wireType 2 =*/138).fork()).ldelim();
            if (message.gaugeDef != null && Object.hasOwnProperty.call(message, "gaugeDef"))
                $root.epoch_proto.GaugeDef.encode(message.gaugeDef, writer.uint32(/* id 18, wireType 2 =*/146).fork()).ldelim();
            if (message.bulletDef != null && Object.hasOwnProperty.call(message, "bulletDef"))
                $root.epoch_proto.BulletDef.encode(message.bulletDef, writer.uint32(/* id 19, wireType 2 =*/154).fork()).ldelim();
            if (message.timelineDef != null && Object.hasOwnProperty.call(message, "timelineDef"))
                $root.epoch_proto.TimelineDef.encode(message.timelineDef, writer.uint32(/* id 20, wireType 2 =*/162).fork()).ldelim();
            if (message.errorBarDef != null && Object.hasOwnProperty.call(message, "errorBarDef"))
                $root.epoch_proto.ErrorBarDef.encode(message.errorBarDef, writer.uint32(/* id 21, wireType 2 =*/170).fork()).ldelim();
            if (message.bellCurveDef != null && Object.hasOwnProperty.call(message, "bellCurveDef"))
                $root.epoch_proto.BellCurveDef.encode(message.bellCurveDef, writer.uint32(/* id 22, wireType 2 =*/178).fork()).ldelim();
            if (message.numericErrorBarDef != null && Object.hasOwnProperty.call(message, "numericErrorBarDef"))
                $root.epoch_proto.NumericErrorBarDef.encode(message.numericErrorBarDef, writer.uint32(/* id 23, wireType 2 =*/186).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified Chart message, length delimited. Does not implicitly {@link epoch_proto.Chart.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.Chart
         * @static
         * @param {epoch_proto.IChart} message Chart message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        Chart.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a Chart message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.Chart
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.Chart} Chart
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Chart.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.Chart();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.linesDef = $root.epoch_proto.LinesDef.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        message.heatMapDef = $root.epoch_proto.HeatMapDef.decode(reader, reader.uint32());
                        break;
                    }
                case 3: {
                        message.barDef = $root.epoch_proto.BarDef.decode(reader, reader.uint32());
                        break;
                    }
                case 4: {
                        message.histogramDef = $root.epoch_proto.HistogramDef.decode(reader, reader.uint32());
                        break;
                    }
                case 5: {
                        message.boxPlotDef = $root.epoch_proto.BoxPlotDef.decode(reader, reader.uint32());
                        break;
                    }
                case 6: {
                        message.xRangeDef = $root.epoch_proto.XRangeDef.decode(reader, reader.uint32());
                        break;
                    }
                case 7: {
                        message.pieDef = $root.epoch_proto.PieDef.decode(reader, reader.uint32());
                        break;
                    }
                case 8: {
                        message.areaDef = $root.epoch_proto.AreaDef.decode(reader, reader.uint32());
                        break;
                    }
                case 9: {
                        message.numericLinesDef = $root.epoch_proto.NumericLinesDef.decode(reader, reader.uint32());
                        break;
                    }
                case 10: {
                        message.scatterDef = $root.epoch_proto.ScatterDef.decode(reader, reader.uint32());
                        break;
                    }
                case 11: {
                        message.waterfallDef = $root.epoch_proto.WaterfallDef.decode(reader, reader.uint32());
                        break;
                    }
                case 12: {
                        message.splineDef = $root.epoch_proto.SplineDef.decode(reader, reader.uint32());
                        break;
                    }
                case 13: {
                        message.numericSplineDef = $root.epoch_proto.NumericSplineDef.decode(reader, reader.uint32());
                        break;
                    }
                case 14: {
                        message.bubbleDef = $root.epoch_proto.BubbleDef.decode(reader, reader.uint32());
                        break;
                    }
                case 15: {
                        message.treemapDef = $root.epoch_proto.TreemapDef.decode(reader, reader.uint32());
                        break;
                    }
                case 16: {
                        message.sankeyDef = $root.epoch_proto.SankeyDef.decode(reader, reader.uint32());
                        break;
                    }
                case 17: {
                        message.areaRangeDef = $root.epoch_proto.AreaRangeDef.decode(reader, reader.uint32());
                        break;
                    }
                case 18: {
                        message.gaugeDef = $root.epoch_proto.GaugeDef.decode(reader, reader.uint32());
                        break;
                    }
                case 19: {
                        message.bulletDef = $root.epoch_proto.BulletDef.decode(reader, reader.uint32());
                        break;
                    }
                case 20: {
                        message.timelineDef = $root.epoch_proto.TimelineDef.decode(reader, reader.uint32());
                        break;
                    }
                case 21: {
                        message.errorBarDef = $root.epoch_proto.ErrorBarDef.decode(reader, reader.uint32());
                        break;
                    }
                case 22: {
                        message.bellCurveDef = $root.epoch_proto.BellCurveDef.decode(reader, reader.uint32());
                        break;
                    }
                case 23: {
                        message.numericErrorBarDef = $root.epoch_proto.NumericErrorBarDef.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a Chart message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.Chart
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.Chart} Chart
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        Chart.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a Chart message.
         * @function verify
         * @memberof epoch_proto.Chart
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        Chart.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            let properties = {};
            if (message.linesDef != null && message.hasOwnProperty("linesDef")) {
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.LinesDef.verify(message.linesDef);
                    if (error)
                        return "linesDef." + error;
                }
            }
            if (message.heatMapDef != null && message.hasOwnProperty("heatMapDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.HeatMapDef.verify(message.heatMapDef);
                    if (error)
                        return "heatMapDef." + error;
                }
            }
            if (message.barDef != null && message.hasOwnProperty("barDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.BarDef.verify(message.barDef);
                    if (error)
                        return "barDef." + error;
                }
            }
            if (message.histogramDef != null && message.hasOwnProperty("histogramDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.HistogramDef.verify(message.histogramDef);
                    if (error)
                        return "histogramDef." + error;
                }
            }
            if (message.boxPlotDef != null && message.hasOwnProperty("boxPlotDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.BoxPlotDef.verify(message.boxPlotDef);
                    if (error)
                        return "boxPlotDef." + error;
                }
            }
            if (message.xRangeDef != null && message.hasOwnProperty("xRangeDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.XRangeDef.verify(message.xRangeDef);
                    if (error)
                        return "xRangeDef." + error;
                }
            }
            if (message.pieDef != null && message.hasOwnProperty("pieDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.PieDef.verify(message.pieDef);
                    if (error)
                        return "pieDef." + error;
                }
            }
            if (message.areaDef != null && message.hasOwnProperty("areaDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.AreaDef.verify(message.areaDef);
                    if (error)
                        return "areaDef." + error;
                }
            }
            if (message.numericLinesDef != null && message.hasOwnProperty("numericLinesDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.NumericLinesDef.verify(message.numericLinesDef);
                    if (error)
                        return "numericLinesDef." + error;
                }
            }
            if (message.scatterDef != null && message.hasOwnProperty("scatterDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.ScatterDef.verify(message.scatterDef);
                    if (error)
                        return "scatterDef." + error;
                }
            }
            if (message.waterfallDef != null && message.hasOwnProperty("waterfallDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.WaterfallDef.verify(message.waterfallDef);
                    if (error)
                        return "waterfallDef." + error;
                }
            }
            if (message.splineDef != null && message.hasOwnProperty("splineDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.SplineDef.verify(message.splineDef);
                    if (error)
                        return "splineDef." + error;
                }
            }
            if (message.numericSplineDef != null && message.hasOwnProperty("numericSplineDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.NumericSplineDef.verify(message.numericSplineDef);
                    if (error)
                        return "numericSplineDef." + error;
                }
            }
            if (message.bubbleDef != null && message.hasOwnProperty("bubbleDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.BubbleDef.verify(message.bubbleDef);
                    if (error)
                        return "bubbleDef." + error;
                }
            }
            if (message.treemapDef != null && message.hasOwnProperty("treemapDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.TreemapDef.verify(message.treemapDef);
                    if (error)
                        return "treemapDef." + error;
                }
            }
            if (message.sankeyDef != null && message.hasOwnProperty("sankeyDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.SankeyDef.verify(message.sankeyDef);
                    if (error)
                        return "sankeyDef." + error;
                }
            }
            if (message.areaRangeDef != null && message.hasOwnProperty("areaRangeDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.AreaRangeDef.verify(message.areaRangeDef);
                    if (error)
                        return "areaRangeDef." + error;
                }
            }
            if (message.gaugeDef != null && message.hasOwnProperty("gaugeDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.GaugeDef.verify(message.gaugeDef);
                    if (error)
                        return "gaugeDef." + error;
                }
            }
            if (message.bulletDef != null && message.hasOwnProperty("bulletDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.BulletDef.verify(message.bulletDef);
                    if (error)
                        return "bulletDef." + error;
                }
            }
            if (message.timelineDef != null && message.hasOwnProperty("timelineDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.TimelineDef.verify(message.timelineDef);
                    if (error)
                        return "timelineDef." + error;
                }
            }
            if (message.errorBarDef != null && message.hasOwnProperty("errorBarDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.ErrorBarDef.verify(message.errorBarDef);
                    if (error)
                        return "errorBarDef." + error;
                }
            }
            if (message.bellCurveDef != null && message.hasOwnProperty("bellCurveDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.BellCurveDef.verify(message.bellCurveDef);
                    if (error)
                        return "bellCurveDef." + error;
                }
            }
            if (message.numericErrorBarDef != null && message.hasOwnProperty("numericErrorBarDef")) {
                if (properties.chartType === 1)
                    return "chartType: multiple values";
                properties.chartType = 1;
                {
                    let error = $root.epoch_proto.NumericErrorBarDef.verify(message.numericErrorBarDef);
                    if (error)
                        return "numericErrorBarDef." + error;
                }
            }
            return null;
        };

        /**
         * Creates a Chart message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.Chart
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.Chart} Chart
         */
        Chart.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.Chart)
                return object;
            let message = new $root.epoch_proto.Chart();
            if (object.linesDef != null) {
                if (typeof object.linesDef !== "object")
                    throw TypeError(".epoch_proto.Chart.linesDef: object expected");
                message.linesDef = $root.epoch_proto.LinesDef.fromObject(object.linesDef);
            }
            if (object.heatMapDef != null) {
                if (typeof object.heatMapDef !== "object")
                    throw TypeError(".epoch_proto.Chart.heatMapDef: object expected");
                message.heatMapDef = $root.epoch_proto.HeatMapDef.fromObject(object.heatMapDef);
            }
            if (object.barDef != null) {
                if (typeof object.barDef !== "object")
                    throw TypeError(".epoch_proto.Chart.barDef: object expected");
                message.barDef = $root.epoch_proto.BarDef.fromObject(object.barDef);
            }
            if (object.histogramDef != null) {
                if (typeof object.histogramDef !== "object")
                    throw TypeError(".epoch_proto.Chart.histogramDef: object expected");
                message.histogramDef = $root.epoch_proto.HistogramDef.fromObject(object.histogramDef);
            }
            if (object.boxPlotDef != null) {
                if (typeof object.boxPlotDef !== "object")
                    throw TypeError(".epoch_proto.Chart.boxPlotDef: object expected");
                message.boxPlotDef = $root.epoch_proto.BoxPlotDef.fromObject(object.boxPlotDef);
            }
            if (object.xRangeDef != null) {
                if (typeof object.xRangeDef !== "object")
                    throw TypeError(".epoch_proto.Chart.xRangeDef: object expected");
                message.xRangeDef = $root.epoch_proto.XRangeDef.fromObject(object.xRangeDef);
            }
            if (object.pieDef != null) {
                if (typeof object.pieDef !== "object")
                    throw TypeError(".epoch_proto.Chart.pieDef: object expected");
                message.pieDef = $root.epoch_proto.PieDef.fromObject(object.pieDef);
            }
            if (object.areaDef != null) {
                if (typeof object.areaDef !== "object")
                    throw TypeError(".epoch_proto.Chart.areaDef: object expected");
                message.areaDef = $root.epoch_proto.AreaDef.fromObject(object.areaDef);
            }
            if (object.numericLinesDef != null) {
                if (typeof object.numericLinesDef !== "object")
                    throw TypeError(".epoch_proto.Chart.numericLinesDef: object expected");
                message.numericLinesDef = $root.epoch_proto.NumericLinesDef.fromObject(object.numericLinesDef);
            }
            if (object.scatterDef != null) {
                if (typeof object.scatterDef !== "object")
                    throw TypeError(".epoch_proto.Chart.scatterDef: object expected");
                message.scatterDef = $root.epoch_proto.ScatterDef.fromObject(object.scatterDef);
            }
            if (object.waterfallDef != null) {
                if (typeof object.waterfallDef !== "object")
                    throw TypeError(".epoch_proto.Chart.waterfallDef: object expected");
                message.waterfallDef = $root.epoch_proto.WaterfallDef.fromObject(object.waterfallDef);
            }
            if (object.splineDef != null) {
                if (typeof object.splineDef !== "object")
                    throw TypeError(".epoch_proto.Chart.splineDef: object expected");
                message.splineDef = $root.epoch_proto.SplineDef.fromObject(object.splineDef);
            }
            if (object.numericSplineDef != null) {
                if (typeof object.numericSplineDef !== "object")
                    throw TypeError(".epoch_proto.Chart.numericSplineDef: object expected");
                message.numericSplineDef = $root.epoch_proto.NumericSplineDef.fromObject(object.numericSplineDef);
            }
            if (object.bubbleDef != null) {
                if (typeof object.bubbleDef !== "object")
                    throw TypeError(".epoch_proto.Chart.bubbleDef: object expected");
                message.bubbleDef = $root.epoch_proto.BubbleDef.fromObject(object.bubbleDef);
            }
            if (object.treemapDef != null) {
                if (typeof object.treemapDef !== "object")
                    throw TypeError(".epoch_proto.Chart.treemapDef: object expected");
                message.treemapDef = $root.epoch_proto.TreemapDef.fromObject(object.treemapDef);
            }
            if (object.sankeyDef != null) {
                if (typeof object.sankeyDef !== "object")
                    throw TypeError(".epoch_proto.Chart.sankeyDef: object expected");
                message.sankeyDef = $root.epoch_proto.SankeyDef.fromObject(object.sankeyDef);
            }
            if (object.areaRangeDef != null) {
                if (typeof object.areaRangeDef !== "object")
                    throw TypeError(".epoch_proto.Chart.areaRangeDef: object expected");
                message.areaRangeDef = $root.epoch_proto.AreaRangeDef.fromObject(object.areaRangeDef);
            }
            if (object.gaugeDef != null) {
                if (typeof object.gaugeDef !== "object")
                    throw TypeError(".epoch_proto.Chart.gaugeDef: object expected");
                message.gaugeDef = $root.epoch_proto.GaugeDef.fromObject(object.gaugeDef);
            }
            if (object.bulletDef != null) {
                if (typeof object.bulletDef !== "object")
                    throw TypeError(".epoch_proto.Chart.bulletDef: object expected");
                message.bulletDef = $root.epoch_proto.BulletDef.fromObject(object.bulletDef);
            }
            if (object.timelineDef != null) {
                if (typeof object.timelineDef !== "object")
                    throw TypeError(".epoch_proto.Chart.timelineDef: object expected");
                message.timelineDef = $root.epoch_proto.TimelineDef.fromObject(object.timelineDef);
            }
            if (object.errorBarDef != null) {
                if (typeof object.errorBarDef !== "object")
                    throw TypeError(".epoch_proto.Chart.errorBarDef: object expected");
                message.errorBarDef = $root.epoch_proto.ErrorBarDef.fromObject(object.errorBarDef);
            }
            if (object.bellCurveDef != null) {
                if (typeof object.bellCurveDef !== "object")
                    throw TypeError(".epoch_proto.Chart.bellCurveDef: object expected");
                message.bellCurveDef = $root.epoch_proto.BellCurveDef.fromObject(object.bellCurveDef);
            }
            if (object.numericErrorBarDef != null) {
                if (typeof object.numericErrorBarDef !== "object")
                    throw TypeError(".epoch_proto.Chart.numericErrorBarDef: object expected");
                message.numericErrorBarDef = $root.epoch_proto.NumericErrorBarDef.fromObject(object.numericErrorBarDef);
            }
            return message;
        };

        /**
         * Creates a plain object from a Chart message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.Chart
         * @static
         * @param {epoch_proto.Chart} message Chart
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        Chart.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (message.linesDef != null && message.hasOwnProperty("linesDef")) {
                object.linesDef = $root.epoch_proto.LinesDef.toObject(message.linesDef, options);
                if (options.oneofs)
                    object.chartType = "linesDef";
            }
            if (message.heatMapDef != null && message.hasOwnProperty("heatMapDef")) {
                object.heatMapDef = $root.epoch_proto.HeatMapDef.toObject(message.heatMapDef, options);
                if (options.oneofs)
                    object.chartType = "heatMapDef";
            }
            if (message.barDef != null && message.hasOwnProperty("barDef")) {
                object.barDef = $root.epoch_proto.BarDef.toObject(message.barDef, options);
                if (options.oneofs)
                    object.chartType = "barDef";
            }
            if (message.histogramDef != null && message.hasOwnProperty("histogramDef")) {
                object.histogramDef = $root.epoch_proto.HistogramDef.toObject(message.histogramDef, options);
                if (options.oneofs)
                    object.chartType = "histogramDef";
            }
            if (message.boxPlotDef != null && message.hasOwnProperty("boxPlotDef")) {
                object.boxPlotDef = $root.epoch_proto.BoxPlotDef.toObject(message.boxPlotDef, options);
                if (options.oneofs)
                    object.chartType = "boxPlotDef";
            }
            if (message.xRangeDef != null && message.hasOwnProperty("xRangeDef")) {
                object.xRangeDef = $root.epoch_proto.XRangeDef.toObject(message.xRangeDef, options);
                if (options.oneofs)
                    object.chartType = "xRangeDef";
            }
            if (message.pieDef != null && message.hasOwnProperty("pieDef")) {
                object.pieDef = $root.epoch_proto.PieDef.toObject(message.pieDef, options);
                if (options.oneofs)
                    object.chartType = "pieDef";
            }
            if (message.areaDef != null && message.hasOwnProperty("areaDef")) {
                object.areaDef = $root.epoch_proto.AreaDef.toObject(message.areaDef, options);
                if (options.oneofs)
                    object.chartType = "areaDef";
            }
            if (message.numericLinesDef != null && message.hasOwnProperty("numericLinesDef")) {
                object.numericLinesDef = $root.epoch_proto.NumericLinesDef.toObject(message.numericLinesDef, options);
                if (options.oneofs)
                    object.chartType = "numericLinesDef";
            }
            if (message.scatterDef != null && message.hasOwnProperty("scatterDef")) {
                object.scatterDef = $root.epoch_proto.ScatterDef.toObject(message.scatterDef, options);
                if (options.oneofs)
                    object.chartType = "scatterDef";
            }
            if (message.waterfallDef != null && message.hasOwnProperty("waterfallDef")) {
                object.waterfallDef = $root.epoch_proto.WaterfallDef.toObject(message.waterfallDef, options);
                if (options.oneofs)
                    object.chartType = "waterfallDef";
            }
            if (message.splineDef != null && message.hasOwnProperty("splineDef")) {
                object.splineDef = $root.epoch_proto.SplineDef.toObject(message.splineDef, options);
                if (options.oneofs)
                    object.chartType = "splineDef";
            }
            if (message.numericSplineDef != null && message.hasOwnProperty("numericSplineDef")) {
                object.numericSplineDef = $root.epoch_proto.NumericSplineDef.toObject(message.numericSplineDef, options);
                if (options.oneofs)
                    object.chartType = "numericSplineDef";
            }
            if (message.bubbleDef != null && message.hasOwnProperty("bubbleDef")) {
                object.bubbleDef = $root.epoch_proto.BubbleDef.toObject(message.bubbleDef, options);
                if (options.oneofs)
                    object.chartType = "bubbleDef";
            }
            if (message.treemapDef != null && message.hasOwnProperty("treemapDef")) {
                object.treemapDef = $root.epoch_proto.TreemapDef.toObject(message.treemapDef, options);
                if (options.oneofs)
                    object.chartType = "treemapDef";
            }
            if (message.sankeyDef != null && message.hasOwnProperty("sankeyDef")) {
                object.sankeyDef = $root.epoch_proto.SankeyDef.toObject(message.sankeyDef, options);
                if (options.oneofs)
                    object.chartType = "sankeyDef";
            }
            if (message.areaRangeDef != null && message.hasOwnProperty("areaRangeDef")) {
                object.areaRangeDef = $root.epoch_proto.AreaRangeDef.toObject(message.areaRangeDef, options);
                if (options.oneofs)
                    object.chartType = "areaRangeDef";
            }
            if (message.gaugeDef != null && message.hasOwnProperty("gaugeDef")) {
                object.gaugeDef = $root.epoch_proto.GaugeDef.toObject(message.gaugeDef, options);
                if (options.oneofs)
                    object.chartType = "gaugeDef";
            }
            if (message.bulletDef != null && message.hasOwnProperty("bulletDef")) {
                object.bulletDef = $root.epoch_proto.BulletDef.toObject(message.bulletDef, options);
                if (options.oneofs)
                    object.chartType = "bulletDef";
            }
            if (message.timelineDef != null && message.hasOwnProperty("timelineDef")) {
                object.timelineDef = $root.epoch_proto.TimelineDef.toObject(message.timelineDef, options);
                if (options.oneofs)
                    object.chartType = "timelineDef";
            }
            if (message.errorBarDef != null && message.hasOwnProperty("errorBarDef")) {
                object.errorBarDef = $root.epoch_proto.ErrorBarDef.toObject(message.errorBarDef, options);
                if (options.oneofs)
                    object.chartType = "errorBarDef";
            }
            if (message.bellCurveDef != null && message.hasOwnProperty("bellCurveDef")) {
                object.bellCurveDef = $root.epoch_proto.BellCurveDef.toObject(message.bellCurveDef, options);
                if (options.oneofs)
                    object.chartType = "bellCurveDef";
            }
            if (message.numericErrorBarDef != null && message.hasOwnProperty("numericErrorBarDef")) {
                object.numericErrorBarDef = $root.epoch_proto.NumericErrorBarDef.toObject(message.numericErrorBarDef, options);
                if (options.oneofs)
                    object.chartType = "numericErrorBarDef";
            }
            return object;
        };

        /**
         * Converts this Chart to JSON.
         * @function toJSON
         * @memberof epoch_proto.Chart
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        Chart.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for Chart
         * @function getTypeUrl
         * @memberof epoch_proto.Chart
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        Chart.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.Chart";
        };

        return Chart;
    })();

    epoch_proto.CardDefList = (function() {

        /**
         * Properties of a CardDefList.
         * @memberof epoch_proto
         * @interface ICardDefList
         * @property {Array.<epoch_proto.ICardDef>|null} [cards] CardDefList cards
         */

        /**
         * Constructs a new CardDefList.
         * @memberof epoch_proto
         * @classdesc Represents a CardDefList.
         * @implements ICardDefList
         * @constructor
         * @param {epoch_proto.ICardDefList=} [properties] Properties to set
         */
        function CardDefList(properties) {
            this.cards = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * CardDefList cards.
         * @member {Array.<epoch_proto.ICardDef>} cards
         * @memberof epoch_proto.CardDefList
         * @instance
         */
        CardDefList.prototype.cards = $util.emptyArray;

        /**
         * Creates a new CardDefList instance using the specified properties.
         * @function create
         * @memberof epoch_proto.CardDefList
         * @static
         * @param {epoch_proto.ICardDefList=} [properties] Properties to set
         * @returns {epoch_proto.CardDefList} CardDefList instance
         */
        CardDefList.create = function create(properties) {
            return new CardDefList(properties);
        };

        /**
         * Encodes the specified CardDefList message. Does not implicitly {@link epoch_proto.CardDefList.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.CardDefList
         * @static
         * @param {epoch_proto.ICardDefList} message CardDefList message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CardDefList.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.cards != null && message.cards.length)
                for (let i = 0; i < message.cards.length; ++i)
                    $root.epoch_proto.CardDef.encode(message.cards[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified CardDefList message, length delimited. Does not implicitly {@link epoch_proto.CardDefList.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.CardDefList
         * @static
         * @param {epoch_proto.ICardDefList} message CardDefList message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        CardDefList.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a CardDefList message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.CardDefList
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.CardDefList} CardDefList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CardDefList.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.CardDefList();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.cards && message.cards.length))
                            message.cards = [];
                        message.cards.push($root.epoch_proto.CardDef.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a CardDefList message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.CardDefList
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.CardDefList} CardDefList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        CardDefList.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a CardDefList message.
         * @function verify
         * @memberof epoch_proto.CardDefList
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        CardDefList.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.cards != null && message.hasOwnProperty("cards")) {
                if (!Array.isArray(message.cards))
                    return "cards: array expected";
                for (let i = 0; i < message.cards.length; ++i) {
                    let error = $root.epoch_proto.CardDef.verify(message.cards[i]);
                    if (error)
                        return "cards." + error;
                }
            }
            return null;
        };

        /**
         * Creates a CardDefList message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.CardDefList
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.CardDefList} CardDefList
         */
        CardDefList.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.CardDefList)
                return object;
            let message = new $root.epoch_proto.CardDefList();
            if (object.cards) {
                if (!Array.isArray(object.cards))
                    throw TypeError(".epoch_proto.CardDefList.cards: array expected");
                message.cards = [];
                for (let i = 0; i < object.cards.length; ++i) {
                    if (typeof object.cards[i] !== "object")
                        throw TypeError(".epoch_proto.CardDefList.cards: object expected");
                    message.cards[i] = $root.epoch_proto.CardDef.fromObject(object.cards[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a CardDefList message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.CardDefList
         * @static
         * @param {epoch_proto.CardDefList} message CardDefList
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        CardDefList.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.cards = [];
            if (message.cards && message.cards.length) {
                object.cards = [];
                for (let j = 0; j < message.cards.length; ++j)
                    object.cards[j] = $root.epoch_proto.CardDef.toObject(message.cards[j], options);
            }
            return object;
        };

        /**
         * Converts this CardDefList to JSON.
         * @function toJSON
         * @memberof epoch_proto.CardDefList
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        CardDefList.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for CardDefList
         * @function getTypeUrl
         * @memberof epoch_proto.CardDefList
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        CardDefList.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.CardDefList";
        };

        return CardDefList;
    })();

    epoch_proto.ChartList = (function() {

        /**
         * Properties of a ChartList.
         * @memberof epoch_proto
         * @interface IChartList
         * @property {Array.<epoch_proto.IChart>|null} [charts] ChartList charts
         */

        /**
         * Constructs a new ChartList.
         * @memberof epoch_proto
         * @classdesc Represents a ChartList.
         * @implements IChartList
         * @constructor
         * @param {epoch_proto.IChartList=} [properties] Properties to set
         */
        function ChartList(properties) {
            this.charts = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ChartList charts.
         * @member {Array.<epoch_proto.IChart>} charts
         * @memberof epoch_proto.ChartList
         * @instance
         */
        ChartList.prototype.charts = $util.emptyArray;

        /**
         * Creates a new ChartList instance using the specified properties.
         * @function create
         * @memberof epoch_proto.ChartList
         * @static
         * @param {epoch_proto.IChartList=} [properties] Properties to set
         * @returns {epoch_proto.ChartList} ChartList instance
         */
        ChartList.create = function create(properties) {
            return new ChartList(properties);
        };

        /**
         * Encodes the specified ChartList message. Does not implicitly {@link epoch_proto.ChartList.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.ChartList
         * @static
         * @param {epoch_proto.IChartList} message ChartList message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ChartList.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.charts != null && message.charts.length)
                for (let i = 0; i < message.charts.length; ++i)
                    $root.epoch_proto.Chart.encode(message.charts[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified ChartList message, length delimited. Does not implicitly {@link epoch_proto.ChartList.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.ChartList
         * @static
         * @param {epoch_proto.IChartList} message ChartList message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ChartList.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ChartList message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.ChartList
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.ChartList} ChartList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ChartList.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.ChartList();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.charts && message.charts.length))
                            message.charts = [];
                        message.charts.push($root.epoch_proto.Chart.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ChartList message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.ChartList
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.ChartList} ChartList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ChartList.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ChartList message.
         * @function verify
         * @memberof epoch_proto.ChartList
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ChartList.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.charts != null && message.hasOwnProperty("charts")) {
                if (!Array.isArray(message.charts))
                    return "charts: array expected";
                for (let i = 0; i < message.charts.length; ++i) {
                    let error = $root.epoch_proto.Chart.verify(message.charts[i]);
                    if (error)
                        return "charts." + error;
                }
            }
            return null;
        };

        /**
         * Creates a ChartList message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.ChartList
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.ChartList} ChartList
         */
        ChartList.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.ChartList)
                return object;
            let message = new $root.epoch_proto.ChartList();
            if (object.charts) {
                if (!Array.isArray(object.charts))
                    throw TypeError(".epoch_proto.ChartList.charts: array expected");
                message.charts = [];
                for (let i = 0; i < object.charts.length; ++i) {
                    if (typeof object.charts[i] !== "object")
                        throw TypeError(".epoch_proto.ChartList.charts: object expected");
                    message.charts[i] = $root.epoch_proto.Chart.fromObject(object.charts[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a ChartList message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.ChartList
         * @static
         * @param {epoch_proto.ChartList} message ChartList
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ChartList.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.charts = [];
            if (message.charts && message.charts.length) {
                object.charts = [];
                for (let j = 0; j < message.charts.length; ++j)
                    object.charts[j] = $root.epoch_proto.Chart.toObject(message.charts[j], options);
            }
            return object;
        };

        /**
         * Converts this ChartList to JSON.
         * @function toJSON
         * @memberof epoch_proto.ChartList
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ChartList.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for ChartList
         * @function getTypeUrl
         * @memberof epoch_proto.ChartList
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        ChartList.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.ChartList";
        };

        return ChartList;
    })();

    epoch_proto.TableList = (function() {

        /**
         * Properties of a TableList.
         * @memberof epoch_proto
         * @interface ITableList
         * @property {Array.<epoch_proto.ITable>|null} [tables] TableList tables
         */

        /**
         * Constructs a new TableList.
         * @memberof epoch_proto
         * @classdesc Represents a TableList.
         * @implements ITableList
         * @constructor
         * @param {epoch_proto.ITableList=} [properties] Properties to set
         */
        function TableList(properties) {
            this.tables = [];
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * TableList tables.
         * @member {Array.<epoch_proto.ITable>} tables
         * @memberof epoch_proto.TableList
         * @instance
         */
        TableList.prototype.tables = $util.emptyArray;

        /**
         * Creates a new TableList instance using the specified properties.
         * @function create
         * @memberof epoch_proto.TableList
         * @static
         * @param {epoch_proto.ITableList=} [properties] Properties to set
         * @returns {epoch_proto.TableList} TableList instance
         */
        TableList.create = function create(properties) {
            return new TableList(properties);
        };

        /**
         * Encodes the specified TableList message. Does not implicitly {@link epoch_proto.TableList.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.TableList
         * @static
         * @param {epoch_proto.ITableList} message TableList message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TableList.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.tables != null && message.tables.length)
                for (let i = 0; i < message.tables.length; ++i)
                    $root.epoch_proto.Table.encode(message.tables[i], writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified TableList message, length delimited. Does not implicitly {@link epoch_proto.TableList.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.TableList
         * @static
         * @param {epoch_proto.ITableList} message TableList message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TableList.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a TableList message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.TableList
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.TableList} TableList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TableList.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.TableList();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (!(message.tables && message.tables.length))
                            message.tables = [];
                        message.tables.push($root.epoch_proto.Table.decode(reader, reader.uint32()));
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a TableList message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.TableList
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.TableList} TableList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TableList.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a TableList message.
         * @function verify
         * @memberof epoch_proto.TableList
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        TableList.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.tables != null && message.hasOwnProperty("tables")) {
                if (!Array.isArray(message.tables))
                    return "tables: array expected";
                for (let i = 0; i < message.tables.length; ++i) {
                    let error = $root.epoch_proto.Table.verify(message.tables[i]);
                    if (error)
                        return "tables." + error;
                }
            }
            return null;
        };

        /**
         * Creates a TableList message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.TableList
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.TableList} TableList
         */
        TableList.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.TableList)
                return object;
            let message = new $root.epoch_proto.TableList();
            if (object.tables) {
                if (!Array.isArray(object.tables))
                    throw TypeError(".epoch_proto.TableList.tables: array expected");
                message.tables = [];
                for (let i = 0; i < object.tables.length; ++i) {
                    if (typeof object.tables[i] !== "object")
                        throw TypeError(".epoch_proto.TableList.tables: object expected");
                    message.tables[i] = $root.epoch_proto.Table.fromObject(object.tables[i]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a TableList message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.TableList
         * @static
         * @param {epoch_proto.TableList} message TableList
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        TableList.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.arrays || options.defaults)
                object.tables = [];
            if (message.tables && message.tables.length) {
                object.tables = [];
                for (let j = 0; j < message.tables.length; ++j)
                    object.tables[j] = $root.epoch_proto.Table.toObject(message.tables[j], options);
            }
            return object;
        };

        /**
         * Converts this TableList to JSON.
         * @function toJSON
         * @memberof epoch_proto.TableList
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        TableList.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for TableList
         * @function getTypeUrl
         * @memberof epoch_proto.TableList
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        TableList.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.TableList";
        };

        return TableList;
    })();

    epoch_proto.TearSheet = (function() {

        /**
         * Properties of a TearSheet.
         * @memberof epoch_proto
         * @interface ITearSheet
         * @property {epoch_proto.ICardDefList|null} [cards] TearSheet cards
         * @property {epoch_proto.IChartList|null} [charts] TearSheet charts
         * @property {epoch_proto.ITableList|null} [tables] TearSheet tables
         */

        /**
         * Constructs a new TearSheet.
         * @memberof epoch_proto
         * @classdesc Represents a TearSheet.
         * @implements ITearSheet
         * @constructor
         * @param {epoch_proto.ITearSheet=} [properties] Properties to set
         */
        function TearSheet(properties) {
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * TearSheet cards.
         * @member {epoch_proto.ICardDefList|null|undefined} cards
         * @memberof epoch_proto.TearSheet
         * @instance
         */
        TearSheet.prototype.cards = null;

        /**
         * TearSheet charts.
         * @member {epoch_proto.IChartList|null|undefined} charts
         * @memberof epoch_proto.TearSheet
         * @instance
         */
        TearSheet.prototype.charts = null;

        /**
         * TearSheet tables.
         * @member {epoch_proto.ITableList|null|undefined} tables
         * @memberof epoch_proto.TearSheet
         * @instance
         */
        TearSheet.prototype.tables = null;

        /**
         * Creates a new TearSheet instance using the specified properties.
         * @function create
         * @memberof epoch_proto.TearSheet
         * @static
         * @param {epoch_proto.ITearSheet=} [properties] Properties to set
         * @returns {epoch_proto.TearSheet} TearSheet instance
         */
        TearSheet.create = function create(properties) {
            return new TearSheet(properties);
        };

        /**
         * Encodes the specified TearSheet message. Does not implicitly {@link epoch_proto.TearSheet.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.TearSheet
         * @static
         * @param {epoch_proto.ITearSheet} message TearSheet message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TearSheet.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.cards != null && Object.hasOwnProperty.call(message, "cards"))
                $root.epoch_proto.CardDefList.encode(message.cards, writer.uint32(/* id 1, wireType 2 =*/10).fork()).ldelim();
            if (message.charts != null && Object.hasOwnProperty.call(message, "charts"))
                $root.epoch_proto.ChartList.encode(message.charts, writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim();
            if (message.tables != null && Object.hasOwnProperty.call(message, "tables"))
                $root.epoch_proto.TableList.encode(message.tables, writer.uint32(/* id 3, wireType 2 =*/26).fork()).ldelim();
            return writer;
        };

        /**
         * Encodes the specified TearSheet message, length delimited. Does not implicitly {@link epoch_proto.TearSheet.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.TearSheet
         * @static
         * @param {epoch_proto.ITearSheet} message TearSheet message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        TearSheet.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a TearSheet message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.TearSheet
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.TearSheet} TearSheet
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TearSheet.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.TearSheet();
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        message.cards = $root.epoch_proto.CardDefList.decode(reader, reader.uint32());
                        break;
                    }
                case 2: {
                        message.charts = $root.epoch_proto.ChartList.decode(reader, reader.uint32());
                        break;
                    }
                case 3: {
                        message.tables = $root.epoch_proto.TableList.decode(reader, reader.uint32());
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a TearSheet message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.TearSheet
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.TearSheet} TearSheet
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        TearSheet.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a TearSheet message.
         * @function verify
         * @memberof epoch_proto.TearSheet
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        TearSheet.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.cards != null && message.hasOwnProperty("cards")) {
                let error = $root.epoch_proto.CardDefList.verify(message.cards);
                if (error)
                    return "cards." + error;
            }
            if (message.charts != null && message.hasOwnProperty("charts")) {
                let error = $root.epoch_proto.ChartList.verify(message.charts);
                if (error)
                    return "charts." + error;
            }
            if (message.tables != null && message.hasOwnProperty("tables")) {
                let error = $root.epoch_proto.TableList.verify(message.tables);
                if (error)
                    return "tables." + error;
            }
            return null;
        };

        /**
         * Creates a TearSheet message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.TearSheet
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.TearSheet} TearSheet
         */
        TearSheet.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.TearSheet)
                return object;
            let message = new $root.epoch_proto.TearSheet();
            if (object.cards != null) {
                if (typeof object.cards !== "object")
                    throw TypeError(".epoch_proto.TearSheet.cards: object expected");
                message.cards = $root.epoch_proto.CardDefList.fromObject(object.cards);
            }
            if (object.charts != null) {
                if (typeof object.charts !== "object")
                    throw TypeError(".epoch_proto.TearSheet.charts: object expected");
                message.charts = $root.epoch_proto.ChartList.fromObject(object.charts);
            }
            if (object.tables != null) {
                if (typeof object.tables !== "object")
                    throw TypeError(".epoch_proto.TearSheet.tables: object expected");
                message.tables = $root.epoch_proto.TableList.fromObject(object.tables);
            }
            return message;
        };

        /**
         * Creates a plain object from a TearSheet message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.TearSheet
         * @static
         * @param {epoch_proto.TearSheet} message TearSheet
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        TearSheet.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.defaults) {
                object.cards = null;
                object.charts = null;
                object.tables = null;
            }
            if (message.cards != null && message.hasOwnProperty("cards"))
                object.cards = $root.epoch_proto.CardDefList.toObject(message.cards, options);
            if (message.charts != null && message.hasOwnProperty("charts"))
                object.charts = $root.epoch_proto.ChartList.toObject(message.charts, options);
            if (message.tables != null && message.hasOwnProperty("tables"))
                object.tables = $root.epoch_proto.TableList.toObject(message.tables, options);
            return object;
        };

        /**
         * Converts this TearSheet to JSON.
         * @function toJSON
         * @memberof epoch_proto.TearSheet
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        TearSheet.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for TearSheet
         * @function getTypeUrl
         * @memberof epoch_proto.TearSheet
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        TearSheet.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.TearSheet";
        };

        return TearSheet;
    })();

    epoch_proto.FullTearSheet = (function() {

        /**
         * Properties of a FullTearSheet.
         * @memberof epoch_proto
         * @interface IFullTearSheet
         * @property {Object.<string,epoch_proto.ITearSheet>|null} [categories] FullTearSheet categories
         */

        /**
         * Constructs a new FullTearSheet.
         * @memberof epoch_proto
         * @classdesc Represents a FullTearSheet.
         * @implements IFullTearSheet
         * @constructor
         * @param {epoch_proto.IFullTearSheet=} [properties] Properties to set
         */
        function FullTearSheet(properties) {
            this.categories = {};
            if (properties)
                for (let keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * FullTearSheet categories.
         * @member {Object.<string,epoch_proto.ITearSheet>} categories
         * @memberof epoch_proto.FullTearSheet
         * @instance
         */
        FullTearSheet.prototype.categories = $util.emptyObject;

        /**
         * Creates a new FullTearSheet instance using the specified properties.
         * @function create
         * @memberof epoch_proto.FullTearSheet
         * @static
         * @param {epoch_proto.IFullTearSheet=} [properties] Properties to set
         * @returns {epoch_proto.FullTearSheet} FullTearSheet instance
         */
        FullTearSheet.create = function create(properties) {
            return new FullTearSheet(properties);
        };

        /**
         * Encodes the specified FullTearSheet message. Does not implicitly {@link epoch_proto.FullTearSheet.verify|verify} messages.
         * @function encode
         * @memberof epoch_proto.FullTearSheet
         * @static
         * @param {epoch_proto.IFullTearSheet} message FullTearSheet message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        FullTearSheet.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.categories != null && Object.hasOwnProperty.call(message, "categories"))
                for (let keys = Object.keys(message.categories), i = 0; i < keys.length; ++i) {
                    writer.uint32(/* id 1, wireType 2 =*/10).fork().uint32(/* id 1, wireType 2 =*/10).string(keys[i]);
                    $root.epoch_proto.TearSheet.encode(message.categories[keys[i]], writer.uint32(/* id 2, wireType 2 =*/18).fork()).ldelim().ldelim();
                }
            return writer;
        };

        /**
         * Encodes the specified FullTearSheet message, length delimited. Does not implicitly {@link epoch_proto.FullTearSheet.verify|verify} messages.
         * @function encodeDelimited
         * @memberof epoch_proto.FullTearSheet
         * @static
         * @param {epoch_proto.IFullTearSheet} message FullTearSheet message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        FullTearSheet.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a FullTearSheet message from the specified reader or buffer.
         * @function decode
         * @memberof epoch_proto.FullTearSheet
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {epoch_proto.FullTearSheet} FullTearSheet
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        FullTearSheet.decode = function decode(reader, length, error) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            let end = length === undefined ? reader.len : reader.pos + length, message = new $root.epoch_proto.FullTearSheet(), key, value;
            while (reader.pos < end) {
                let tag = reader.uint32();
                if (tag === error)
                    break;
                switch (tag >>> 3) {
                case 1: {
                        if (message.categories === $util.emptyObject)
                            message.categories = {};
                        let end2 = reader.uint32() + reader.pos;
                        key = "";
                        value = null;
                        while (reader.pos < end2) {
                            let tag2 = reader.uint32();
                            switch (tag2 >>> 3) {
                            case 1:
                                key = reader.string();
                                break;
                            case 2:
                                value = $root.epoch_proto.TearSheet.decode(reader, reader.uint32());
                                break;
                            default:
                                reader.skipType(tag2 & 7);
                                break;
                            }
                        }
                        message.categories[key] = value;
                        break;
                    }
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a FullTearSheet message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof epoch_proto.FullTearSheet
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {epoch_proto.FullTearSheet} FullTearSheet
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        FullTearSheet.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a FullTearSheet message.
         * @function verify
         * @memberof epoch_proto.FullTearSheet
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        FullTearSheet.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.categories != null && message.hasOwnProperty("categories")) {
                if (!$util.isObject(message.categories))
                    return "categories: object expected";
                let key = Object.keys(message.categories);
                for (let i = 0; i < key.length; ++i) {
                    let error = $root.epoch_proto.TearSheet.verify(message.categories[key[i]]);
                    if (error)
                        return "categories." + error;
                }
            }
            return null;
        };

        /**
         * Creates a FullTearSheet message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof epoch_proto.FullTearSheet
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {epoch_proto.FullTearSheet} FullTearSheet
         */
        FullTearSheet.fromObject = function fromObject(object) {
            if (object instanceof $root.epoch_proto.FullTearSheet)
                return object;
            let message = new $root.epoch_proto.FullTearSheet();
            if (object.categories) {
                if (typeof object.categories !== "object")
                    throw TypeError(".epoch_proto.FullTearSheet.categories: object expected");
                message.categories = {};
                for (let keys = Object.keys(object.categories), i = 0; i < keys.length; ++i) {
                    if (typeof object.categories[keys[i]] !== "object")
                        throw TypeError(".epoch_proto.FullTearSheet.categories: object expected");
                    message.categories[keys[i]] = $root.epoch_proto.TearSheet.fromObject(object.categories[keys[i]]);
                }
            }
            return message;
        };

        /**
         * Creates a plain object from a FullTearSheet message. Also converts values to other types if specified.
         * @function toObject
         * @memberof epoch_proto.FullTearSheet
         * @static
         * @param {epoch_proto.FullTearSheet} message FullTearSheet
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        FullTearSheet.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            let object = {};
            if (options.objects || options.defaults)
                object.categories = {};
            let keys2;
            if (message.categories && (keys2 = Object.keys(message.categories)).length) {
                object.categories = {};
                for (let j = 0; j < keys2.length; ++j)
                    object.categories[keys2[j]] = $root.epoch_proto.TearSheet.toObject(message.categories[keys2[j]], options);
            }
            return object;
        };

        /**
         * Converts this FullTearSheet to JSON.
         * @function toJSON
         * @memberof epoch_proto.FullTearSheet
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        FullTearSheet.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        /**
         * Gets the default type url for FullTearSheet
         * @function getTypeUrl
         * @memberof epoch_proto.FullTearSheet
         * @static
         * @param {string} [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns {string} The default type url
         */
        FullTearSheet.getTypeUrl = function getTypeUrl(typeUrlPrefix) {
            if (typeUrlPrefix === undefined) {
                typeUrlPrefix = "type.googleapis.com";
            }
            return typeUrlPrefix + "/epoch_proto.FullTearSheet";
        };

        return FullTearSheet;
    })();

    return epoch_proto;
})();

export default $root;
