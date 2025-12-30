import * as $protobuf from "protobufjs";
import Long = require("long");
/** Namespace epoch_proto. */
export namespace epoch_proto {

    /** EpochFolioDashboardWidget enum. */
    enum EpochFolioDashboardWidget {
        WidgetUnspecified = 0,
        WidgetCard = 1,
        WidgetLines = 2,
        WidgetBar = 3,
        WidgetDataTable = 4,
        WidgetXRange = 5,
        WidgetHistogram = 6,
        WidgetPie = 7,
        WidgetHeatMap = 8,
        WidgetBoxPlot = 9,
        WidgetArea = 10,
        WidgetColumn = 11,
        WidgetScatter = 12,
        WidgetWaterfall = 13,
        WidgetSpline = 14,
        WidgetBubble = 15,
        WidgetTreemap = 16,
        WidgetSankey = 17,
        WidgetAreaRange = 18,
        WidgetGauge = 19,
        WidgetBullet = 20,
        WidgetTimeline = 21,
        WidgetErrorBar = 22,
        WidgetBellCurve = 23,
        WidgetNumericErrorBar = 24
    }

    /** EpochFolioType enum. */
    enum EpochFolioType {
        TypeUnspecified = 0,
        TypeString = 1,
        TypeInteger = 2,
        TypeDecimal = 3,
        TypePercent = 4,
        TypeBoolean = 5,
        TypeDateTime = 6,
        TypeDate = 7,
        TypeDayDuration = 8,
        TypeMonetary = 9,
        TypeDuration = 10
    }

    /** NullValue enum. */
    enum NullValue {
        NULL_VALUE = 0
    }

    /** Properties of a Scalar. */
    interface IScalar {

        /** Scalar stringValue */
        stringValue?: (string|null);

        /** Scalar integerValue */
        integerValue?: (number|Long|null);

        /** Scalar decimalValue */
        decimalValue?: (number|null);

        /** Scalar percentValue */
        percentValue?: (number|null);

        /** Scalar booleanValue */
        booleanValue?: (boolean|null);

        /** Scalar timestampMs */
        timestampMs?: (number|Long|null);

        /** Scalar dateValue */
        dateValue?: (number|Long|null);

        /** Scalar dayDuration */
        dayDuration?: (number|null);

        /** Scalar monetaryValue */
        monetaryValue?: (number|null);

        /** Scalar durationMs */
        durationMs?: (number|Long|null);

        /** Scalar nullValue */
        nullValue?: (epoch_proto.NullValue|null);
    }

    /** Represents a Scalar. */
    class Scalar implements IScalar {

        /**
         * Constructs a new Scalar.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IScalar);

        /** Scalar stringValue. */
        public stringValue?: (string|null);

        /** Scalar integerValue. */
        public integerValue?: (number|Long|null);

        /** Scalar decimalValue. */
        public decimalValue?: (number|null);

        /** Scalar percentValue. */
        public percentValue?: (number|null);

        /** Scalar booleanValue. */
        public booleanValue?: (boolean|null);

        /** Scalar timestampMs. */
        public timestampMs?: (number|Long|null);

        /** Scalar dateValue. */
        public dateValue?: (number|Long|null);

        /** Scalar dayDuration. */
        public dayDuration?: (number|null);

        /** Scalar monetaryValue. */
        public monetaryValue?: (number|null);

        /** Scalar durationMs. */
        public durationMs?: (number|Long|null);

        /** Scalar nullValue. */
        public nullValue?: (epoch_proto.NullValue|null);

        /** Scalar value. */
        public value?: ("stringValue"|"integerValue"|"decimalValue"|"percentValue"|"booleanValue"|"timestampMs"|"dateValue"|"dayDuration"|"monetaryValue"|"durationMs"|"nullValue");

        /**
         * Creates a new Scalar instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Scalar instance
         */
        public static create(properties?: epoch_proto.IScalar): epoch_proto.Scalar;

        /**
         * Encodes the specified Scalar message. Does not implicitly {@link epoch_proto.Scalar.verify|verify} messages.
         * @param message Scalar message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IScalar, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Scalar message, length delimited. Does not implicitly {@link epoch_proto.Scalar.verify|verify} messages.
         * @param message Scalar message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IScalar, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a Scalar message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Scalar
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.Scalar;

        /**
         * Decodes a Scalar message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Scalar
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.Scalar;

        /**
         * Verifies a Scalar message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a Scalar message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Scalar
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.Scalar;

        /**
         * Creates a plain object from a Scalar message. Also converts values to other types if specified.
         * @param message Scalar
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.Scalar, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Scalar to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for Scalar
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of an Array. */
    interface IArray {

        /** Array values */
        values?: (epoch_proto.IScalar[]|null);
    }

    /** Represents an Array. */
    class Array implements IArray {

        /**
         * Constructs a new Array.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IArray);

        /** Array values. */
        public values: epoch_proto.IScalar[];

        /**
         * Creates a new Array instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Array instance
         */
        public static create(properties?: epoch_proto.IArray): epoch_proto.Array;

        /**
         * Encodes the specified Array message. Does not implicitly {@link epoch_proto.Array.verify|verify} messages.
         * @param message Array message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IArray, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Array message, length delimited. Does not implicitly {@link epoch_proto.Array.verify|verify} messages.
         * @param message Array message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IArray, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an Array message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Array
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.Array;

        /**
         * Decodes an Array message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Array
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.Array;

        /**
         * Verifies an Array message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an Array message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Array
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.Array;

        /**
         * Creates a plain object from an Array message. Also converts values to other types if specified.
         * @param message Array
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.Array, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Array to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for Array
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** AxisType enum. */
    enum AxisType {
        AxisUnspecified = 0,
        AxisLinear = 1,
        AxisLogarithmic = 2,
        AxisDateTime = 3,
        AxisCategory = 4
    }

    /** DashStyle enum. */
    enum DashStyle {
        DashStyleUnspecified = 0,
        Solid = 1,
        ShortDash = 2,
        ShortDot = 3,
        ShortDashDot = 4,
        ShortDashDotDot = 5,
        Dot = 6,
        Dash = 7,
        LongDash = 8,
        DashDot = 9,
        LongDashDot = 10,
        LongDashDotDot = 11
    }

    /** Properties of an AxisDef. */
    interface IAxisDef {

        /** AxisDef type */
        type?: (epoch_proto.AxisType|null);

        /** AxisDef label */
        label?: (string|null);

        /** AxisDef categories */
        categories?: (string[]|null);
    }

    /** Represents an AxisDef. */
    class AxisDef implements IAxisDef {

        /**
         * Constructs a new AxisDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IAxisDef);

        /** AxisDef type. */
        public type?: (epoch_proto.AxisType|null);

        /** AxisDef label. */
        public label?: (string|null);

        /** AxisDef categories. */
        public categories: string[];

        /**
         * Creates a new AxisDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns AxisDef instance
         */
        public static create(properties?: epoch_proto.IAxisDef): epoch_proto.AxisDef;

        /**
         * Encodes the specified AxisDef message. Does not implicitly {@link epoch_proto.AxisDef.verify|verify} messages.
         * @param message AxisDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IAxisDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified AxisDef message, length delimited. Does not implicitly {@link epoch_proto.AxisDef.verify|verify} messages.
         * @param message AxisDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IAxisDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an AxisDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns AxisDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.AxisDef;

        /**
         * Decodes an AxisDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns AxisDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.AxisDef;

        /**
         * Verifies an AxisDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an AxisDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns AxisDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.AxisDef;

        /**
         * Creates a plain object from an AxisDef message. Also converts values to other types if specified.
         * @param message AxisDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.AxisDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this AxisDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for AxisDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a ChartDef. */
    interface IChartDef {

        /** ChartDef id */
        id?: (string|null);

        /** ChartDef title */
        title?: (string|null);

        /** ChartDef type */
        type?: (epoch_proto.EpochFolioDashboardWidget|null);

        /** ChartDef category */
        category?: (string|null);

        /** ChartDef yAxis */
        yAxis?: (epoch_proto.IAxisDef|null);

        /** ChartDef xAxis */
        xAxis?: (epoch_proto.IAxisDef|null);
    }

    /** Represents a ChartDef. */
    class ChartDef implements IChartDef {

        /**
         * Constructs a new ChartDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IChartDef);

        /** ChartDef id. */
        public id: string;

        /** ChartDef title. */
        public title: string;

        /** ChartDef type. */
        public type: epoch_proto.EpochFolioDashboardWidget;

        /** ChartDef category. */
        public category: string;

        /** ChartDef yAxis. */
        public yAxis?: (epoch_proto.IAxisDef|null);

        /** ChartDef xAxis. */
        public xAxis?: (epoch_proto.IAxisDef|null);

        /**
         * Creates a new ChartDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ChartDef instance
         */
        public static create(properties?: epoch_proto.IChartDef): epoch_proto.ChartDef;

        /**
         * Encodes the specified ChartDef message. Does not implicitly {@link epoch_proto.ChartDef.verify|verify} messages.
         * @param message ChartDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IChartDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ChartDef message, length delimited. Does not implicitly {@link epoch_proto.ChartDef.verify|verify} messages.
         * @param message ChartDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IChartDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a ChartDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ChartDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.ChartDef;

        /**
         * Decodes a ChartDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ChartDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.ChartDef;

        /**
         * Verifies a ChartDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a ChartDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ChartDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.ChartDef;

        /**
         * Creates a plain object from a ChartDef message. Also converts values to other types if specified.
         * @param message ChartDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.ChartDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ChartDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for ChartDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a StraightLineDef. */
    interface IStraightLineDef {

        /** StraightLineDef title */
        title?: (string|null);

        /** StraightLineDef value */
        value?: (number|null);

        /** StraightLineDef vertical */
        vertical?: (boolean|null);
    }

    /** Represents a StraightLineDef. */
    class StraightLineDef implements IStraightLineDef {

        /**
         * Constructs a new StraightLineDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IStraightLineDef);

        /** StraightLineDef title. */
        public title: string;

        /** StraightLineDef value. */
        public value: number;

        /** StraightLineDef vertical. */
        public vertical: boolean;

        /**
         * Creates a new StraightLineDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns StraightLineDef instance
         */
        public static create(properties?: epoch_proto.IStraightLineDef): epoch_proto.StraightLineDef;

        /**
         * Encodes the specified StraightLineDef message. Does not implicitly {@link epoch_proto.StraightLineDef.verify|verify} messages.
         * @param message StraightLineDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IStraightLineDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified StraightLineDef message, length delimited. Does not implicitly {@link epoch_proto.StraightLineDef.verify|verify} messages.
         * @param message StraightLineDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IStraightLineDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a StraightLineDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns StraightLineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.StraightLineDef;

        /**
         * Decodes a StraightLineDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns StraightLineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.StraightLineDef;

        /**
         * Verifies a StraightLineDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a StraightLineDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns StraightLineDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.StraightLineDef;

        /**
         * Creates a plain object from a StraightLineDef message. Also converts values to other types if specified.
         * @param message StraightLineDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.StraightLineDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this StraightLineDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for StraightLineDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a Band. */
    interface IBand {

        /** Band from */
        from?: (epoch_proto.IScalar|null);

        /** Band to */
        to?: (epoch_proto.IScalar|null);
    }

    /** Represents a Band. */
    class Band implements IBand {

        /**
         * Constructs a new Band.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBand);

        /** Band from. */
        public from?: (epoch_proto.IScalar|null);

        /** Band to. */
        public to?: (epoch_proto.IScalar|null);

        /**
         * Creates a new Band instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Band instance
         */
        public static create(properties?: epoch_proto.IBand): epoch_proto.Band;

        /**
         * Encodes the specified Band message. Does not implicitly {@link epoch_proto.Band.verify|verify} messages.
         * @param message Band message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBand, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Band message, length delimited. Does not implicitly {@link epoch_proto.Band.verify|verify} messages.
         * @param message Band message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBand, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a Band message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Band
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.Band;

        /**
         * Decodes a Band message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Band
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.Band;

        /**
         * Verifies a Band message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a Band message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Band
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.Band;

        /**
         * Creates a plain object from a Band message. Also converts values to other types if specified.
         * @param message Band
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.Band, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Band to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for Band
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a Point. */
    interface IPoint {

        /** Point x */
        x?: (number|Long|null);

        /** Point y */
        y?: (number|null);
    }

    /** Represents a Point. */
    class Point implements IPoint {

        /**
         * Constructs a new Point.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IPoint);

        /** Point x. */
        public x: (number|Long);

        /** Point y. */
        public y: number;

        /**
         * Creates a new Point instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Point instance
         */
        public static create(properties?: epoch_proto.IPoint): epoch_proto.Point;

        /**
         * Encodes the specified Point message. Does not implicitly {@link epoch_proto.Point.verify|verify} messages.
         * @param message Point message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Point message, length delimited. Does not implicitly {@link epoch_proto.Point.verify|verify} messages.
         * @param message Point message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a Point message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Point
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.Point;

        /**
         * Decodes a Point message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Point
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.Point;

        /**
         * Verifies a Point message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a Point message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Point
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.Point;

        /**
         * Creates a plain object from a Point message. Also converts values to other types if specified.
         * @param message Point
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.Point, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Point to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for Point
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a NumericPoint. */
    interface INumericPoint {

        /** NumericPoint x */
        x?: (number|null);

        /** NumericPoint y */
        y?: (number|null);
    }

    /** Represents a NumericPoint. */
    class NumericPoint implements INumericPoint {

        /**
         * Constructs a new NumericPoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.INumericPoint);

        /** NumericPoint x. */
        public x: number;

        /** NumericPoint y. */
        public y: number;

        /**
         * Creates a new NumericPoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns NumericPoint instance
         */
        public static create(properties?: epoch_proto.INumericPoint): epoch_proto.NumericPoint;

        /**
         * Encodes the specified NumericPoint message. Does not implicitly {@link epoch_proto.NumericPoint.verify|verify} messages.
         * @param message NumericPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.INumericPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified NumericPoint message, length delimited. Does not implicitly {@link epoch_proto.NumericPoint.verify|verify} messages.
         * @param message NumericPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.INumericPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a NumericPoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns NumericPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.NumericPoint;

        /**
         * Decodes a NumericPoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns NumericPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.NumericPoint;

        /**
         * Verifies a NumericPoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a NumericPoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns NumericPoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.NumericPoint;

        /**
         * Creates a plain object from a NumericPoint message. Also converts values to other types if specified.
         * @param message NumericPoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.NumericPoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this NumericPoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for NumericPoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a Line. */
    interface ILine {

        /** Line data */
        data?: (epoch_proto.IPoint[]|null);

        /** Line name */
        name?: (string|null);

        /** Line dashStyle */
        dashStyle?: (epoch_proto.DashStyle|null);

        /** Line lineWidth */
        lineWidth?: (number|null);
    }

    /** Represents a Line. */
    class Line implements ILine {

        /**
         * Constructs a new Line.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ILine);

        /** Line data. */
        public data: epoch_proto.IPoint[];

        /** Line name. */
        public name: string;

        /** Line dashStyle. */
        public dashStyle?: (epoch_proto.DashStyle|null);

        /** Line lineWidth. */
        public lineWidth?: (number|null);

        /**
         * Creates a new Line instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Line instance
         */
        public static create(properties?: epoch_proto.ILine): epoch_proto.Line;

        /**
         * Encodes the specified Line message. Does not implicitly {@link epoch_proto.Line.verify|verify} messages.
         * @param message Line message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ILine, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Line message, length delimited. Does not implicitly {@link epoch_proto.Line.verify|verify} messages.
         * @param message Line message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ILine, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a Line message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Line
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.Line;

        /**
         * Decodes a Line message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Line
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.Line;

        /**
         * Verifies a Line message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a Line message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Line
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.Line;

        /**
         * Creates a plain object from a Line message. Also converts values to other types if specified.
         * @param message Line
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.Line, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Line to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for Line
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a NumericLine. */
    interface INumericLine {

        /** NumericLine data */
        data?: (epoch_proto.INumericPoint[]|null);

        /** NumericLine name */
        name?: (string|null);

        /** NumericLine dashStyle */
        dashStyle?: (epoch_proto.DashStyle|null);

        /** NumericLine lineWidth */
        lineWidth?: (number|null);
    }

    /** Represents a NumericLine. */
    class NumericLine implements INumericLine {

        /**
         * Constructs a new NumericLine.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.INumericLine);

        /** NumericLine data. */
        public data: epoch_proto.INumericPoint[];

        /** NumericLine name. */
        public name: string;

        /** NumericLine dashStyle. */
        public dashStyle?: (epoch_proto.DashStyle|null);

        /** NumericLine lineWidth. */
        public lineWidth?: (number|null);

        /**
         * Creates a new NumericLine instance using the specified properties.
         * @param [properties] Properties to set
         * @returns NumericLine instance
         */
        public static create(properties?: epoch_proto.INumericLine): epoch_proto.NumericLine;

        /**
         * Encodes the specified NumericLine message. Does not implicitly {@link epoch_proto.NumericLine.verify|verify} messages.
         * @param message NumericLine message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.INumericLine, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified NumericLine message, length delimited. Does not implicitly {@link epoch_proto.NumericLine.verify|verify} messages.
         * @param message NumericLine message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.INumericLine, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a NumericLine message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns NumericLine
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.NumericLine;

        /**
         * Decodes a NumericLine message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns NumericLine
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.NumericLine;

        /**
         * Verifies a NumericLine message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a NumericLine message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns NumericLine
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.NumericLine;

        /**
         * Creates a plain object from a NumericLine message. Also converts values to other types if specified.
         * @param message NumericLine
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.NumericLine, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this NumericLine to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for NumericLine
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** StackType enum. */
    enum StackType {
        StackTypeUnspecified = 0,
        StackTypeNormal = 1,
        StackTypePercent = 2
    }

    /** Properties of a ColumnDef. */
    interface IColumnDef {

        /** ColumnDef id */
        id?: (string|null);

        /** ColumnDef name */
        name?: (string|null);

        /** ColumnDef type */
        type?: (epoch_proto.EpochFolioType|null);

        /** ColumnDef decimalPlaces */
        decimalPlaces?: (number|null);
    }

    /** Represents a ColumnDef. */
    class ColumnDef implements IColumnDef {

        /**
         * Constructs a new ColumnDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IColumnDef);

        /** ColumnDef id. */
        public id: string;

        /** ColumnDef name. */
        public name: string;

        /** ColumnDef type. */
        public type: epoch_proto.EpochFolioType;

        /** ColumnDef decimalPlaces. */
        public decimalPlaces?: (number|null);

        /**
         * Creates a new ColumnDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ColumnDef instance
         */
        public static create(properties?: epoch_proto.IColumnDef): epoch_proto.ColumnDef;

        /**
         * Encodes the specified ColumnDef message. Does not implicitly {@link epoch_proto.ColumnDef.verify|verify} messages.
         * @param message ColumnDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IColumnDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ColumnDef message, length delimited. Does not implicitly {@link epoch_proto.ColumnDef.verify|verify} messages.
         * @param message ColumnDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IColumnDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a ColumnDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ColumnDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.ColumnDef;

        /**
         * Decodes a ColumnDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ColumnDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.ColumnDef;

        /**
         * Verifies a ColumnDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a ColumnDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ColumnDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.ColumnDef;

        /**
         * Creates a plain object from a ColumnDef message. Also converts values to other types if specified.
         * @param message ColumnDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.ColumnDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ColumnDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for ColumnDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a TableRow. */
    interface ITableRow {

        /** TableRow values */
        values?: (epoch_proto.IScalar[]|null);
    }

    /** Represents a TableRow. */
    class TableRow implements ITableRow {

        /**
         * Constructs a new TableRow.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ITableRow);

        /** TableRow values. */
        public values: epoch_proto.IScalar[];

        /**
         * Creates a new TableRow instance using the specified properties.
         * @param [properties] Properties to set
         * @returns TableRow instance
         */
        public static create(properties?: epoch_proto.ITableRow): epoch_proto.TableRow;

        /**
         * Encodes the specified TableRow message. Does not implicitly {@link epoch_proto.TableRow.verify|verify} messages.
         * @param message TableRow message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ITableRow, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified TableRow message, length delimited. Does not implicitly {@link epoch_proto.TableRow.verify|verify} messages.
         * @param message TableRow message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ITableRow, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a TableRow message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns TableRow
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.TableRow;

        /**
         * Decodes a TableRow message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns TableRow
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.TableRow;

        /**
         * Verifies a TableRow message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a TableRow message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns TableRow
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.TableRow;

        /**
         * Creates a plain object from a TableRow message. Also converts values to other types if specified.
         * @param message TableRow
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.TableRow, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this TableRow to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for TableRow
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a TableData. */
    interface ITableData {

        /** TableData rows */
        rows?: (epoch_proto.ITableRow[]|null);
    }

    /** Represents a TableData. */
    class TableData implements ITableData {

        /**
         * Constructs a new TableData.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ITableData);

        /** TableData rows. */
        public rows: epoch_proto.ITableRow[];

        /**
         * Creates a new TableData instance using the specified properties.
         * @param [properties] Properties to set
         * @returns TableData instance
         */
        public static create(properties?: epoch_proto.ITableData): epoch_proto.TableData;

        /**
         * Encodes the specified TableData message. Does not implicitly {@link epoch_proto.TableData.verify|verify} messages.
         * @param message TableData message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ITableData, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified TableData message, length delimited. Does not implicitly {@link epoch_proto.TableData.verify|verify} messages.
         * @param message TableData message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ITableData, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a TableData message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns TableData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.TableData;

        /**
         * Decodes a TableData message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns TableData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.TableData;

        /**
         * Verifies a TableData message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a TableData message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns TableData
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.TableData;

        /**
         * Creates a plain object from a TableData message. Also converts values to other types if specified.
         * @param message TableData
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.TableData, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this TableData to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for TableData
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a Table. */
    interface ITable {

        /** Table type */
        type?: (epoch_proto.EpochFolioDashboardWidget|null);

        /** Table category */
        category?: (string|null);

        /** Table title */
        title?: (string|null);

        /** Table columns */
        columns?: (epoch_proto.IColumnDef[]|null);

        /** Table data */
        data?: (epoch_proto.ITableData|null);
    }

    /** Represents a Table. */
    class Table implements ITable {

        /**
         * Constructs a new Table.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ITable);

        /** Table type. */
        public type: epoch_proto.EpochFolioDashboardWidget;

        /** Table category. */
        public category: string;

        /** Table title. */
        public title: string;

        /** Table columns. */
        public columns: epoch_proto.IColumnDef[];

        /** Table data. */
        public data?: (epoch_proto.ITableData|null);

        /**
         * Creates a new Table instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Table instance
         */
        public static create(properties?: epoch_proto.ITable): epoch_proto.Table;

        /**
         * Encodes the specified Table message. Does not implicitly {@link epoch_proto.Table.verify|verify} messages.
         * @param message Table message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ITable, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Table message, length delimited. Does not implicitly {@link epoch_proto.Table.verify|verify} messages.
         * @param message Table message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ITable, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a Table message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Table
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.Table;

        /**
         * Decodes a Table message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Table
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.Table;

        /**
         * Verifies a Table message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a Table message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Table
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.Table;

        /**
         * Creates a plain object from a Table message. Also converts values to other types if specified.
         * @param message Table
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.Table, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Table to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for Table
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a CardData. */
    interface ICardData {

        /** CardData title */
        title?: (string|null);

        /** CardData value */
        value?: (epoch_proto.IScalar|null);

        /** CardData type */
        type?: (epoch_proto.EpochFolioType|null);

        /** CardData group */
        group?: (number|Long|null);

        /** CardData decimalPlaces */
        decimalPlaces?: (number|null);
    }

    /** Represents a CardData. */
    class CardData implements ICardData {

        /**
         * Constructs a new CardData.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ICardData);

        /** CardData title. */
        public title: string;

        /** CardData value. */
        public value?: (epoch_proto.IScalar|null);

        /** CardData type. */
        public type: epoch_proto.EpochFolioType;

        /** CardData group. */
        public group: (number|Long);

        /** CardData decimalPlaces. */
        public decimalPlaces?: (number|null);

        /**
         * Creates a new CardData instance using the specified properties.
         * @param [properties] Properties to set
         * @returns CardData instance
         */
        public static create(properties?: epoch_proto.ICardData): epoch_proto.CardData;

        /**
         * Encodes the specified CardData message. Does not implicitly {@link epoch_proto.CardData.verify|verify} messages.
         * @param message CardData message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ICardData, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified CardData message, length delimited. Does not implicitly {@link epoch_proto.CardData.verify|verify} messages.
         * @param message CardData message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ICardData, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a CardData message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns CardData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.CardData;

        /**
         * Decodes a CardData message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns CardData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.CardData;

        /**
         * Verifies a CardData message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a CardData message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns CardData
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.CardData;

        /**
         * Creates a plain object from a CardData message. Also converts values to other types if specified.
         * @param message CardData
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.CardData, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this CardData to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for CardData
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a CardDef. */
    interface ICardDef {

        /** CardDef type */
        type?: (epoch_proto.EpochFolioDashboardWidget|null);

        /** CardDef category */
        category?: (string|null);

        /** CardDef data */
        data?: (epoch_proto.ICardData[]|null);

        /** CardDef groupSize */
        groupSize?: (number|Long|null);
    }

    /** Represents a CardDef. */
    class CardDef implements ICardDef {

        /**
         * Constructs a new CardDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ICardDef);

        /** CardDef type. */
        public type: epoch_proto.EpochFolioDashboardWidget;

        /** CardDef category. */
        public category: string;

        /** CardDef data. */
        public data: epoch_proto.ICardData[];

        /** CardDef groupSize. */
        public groupSize: (number|Long);

        /**
         * Creates a new CardDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns CardDef instance
         */
        public static create(properties?: epoch_proto.ICardDef): epoch_proto.CardDef;

        /**
         * Encodes the specified CardDef message. Does not implicitly {@link epoch_proto.CardDef.verify|verify} messages.
         * @param message CardDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ICardDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified CardDef message, length delimited. Does not implicitly {@link epoch_proto.CardDef.verify|verify} messages.
         * @param message CardDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ICardDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a CardDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns CardDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.CardDef;

        /**
         * Decodes a CardDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns CardDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.CardDef;

        /**
         * Verifies a CardDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a CardDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns CardDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.CardDef;

        /**
         * Creates a plain object from a CardDef message. Also converts values to other types if specified.
         * @param message CardDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.CardDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this CardDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for CardDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a LinesDef. */
    interface ILinesDef {

        /** LinesDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** LinesDef lines */
        lines?: (epoch_proto.ILine[]|null);

        /** LinesDef straightLines */
        straightLines?: (epoch_proto.IStraightLineDef[]|null);

        /** LinesDef yPlotBands */
        yPlotBands?: (epoch_proto.IBand[]|null);

        /** LinesDef xPlotBands */
        xPlotBands?: (epoch_proto.IBand[]|null);

        /** LinesDef overlay */
        overlay?: (epoch_proto.ILine|null);

        /** LinesDef stacked */
        stacked?: (boolean|null);
    }

    /** Represents a LinesDef. */
    class LinesDef implements ILinesDef {

        /**
         * Constructs a new LinesDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ILinesDef);

        /** LinesDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** LinesDef lines. */
        public lines: epoch_proto.ILine[];

        /** LinesDef straightLines. */
        public straightLines: epoch_proto.IStraightLineDef[];

        /** LinesDef yPlotBands. */
        public yPlotBands: epoch_proto.IBand[];

        /** LinesDef xPlotBands. */
        public xPlotBands: epoch_proto.IBand[];

        /** LinesDef overlay. */
        public overlay?: (epoch_proto.ILine|null);

        /** LinesDef stacked. */
        public stacked: boolean;

        /**
         * Creates a new LinesDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns LinesDef instance
         */
        public static create(properties?: epoch_proto.ILinesDef): epoch_proto.LinesDef;

        /**
         * Encodes the specified LinesDef message. Does not implicitly {@link epoch_proto.LinesDef.verify|verify} messages.
         * @param message LinesDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ILinesDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified LinesDef message, length delimited. Does not implicitly {@link epoch_proto.LinesDef.verify|verify} messages.
         * @param message LinesDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ILinesDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a LinesDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns LinesDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.LinesDef;

        /**
         * Decodes a LinesDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns LinesDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.LinesDef;

        /**
         * Verifies a LinesDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a LinesDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns LinesDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.LinesDef;

        /**
         * Creates a plain object from a LinesDef message. Also converts values to other types if specified.
         * @param message LinesDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.LinesDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this LinesDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for LinesDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a NumericLinesDef. */
    interface INumericLinesDef {

        /** NumericLinesDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** NumericLinesDef lines */
        lines?: (epoch_proto.INumericLine[]|null);

        /** NumericLinesDef straightLines */
        straightLines?: (epoch_proto.IStraightLineDef[]|null);

        /** NumericLinesDef yPlotBands */
        yPlotBands?: (epoch_proto.IBand[]|null);

        /** NumericLinesDef xPlotBands */
        xPlotBands?: (epoch_proto.IBand[]|null);

        /** NumericLinesDef overlay */
        overlay?: (epoch_proto.INumericLine|null);

        /** NumericLinesDef stacked */
        stacked?: (boolean|null);
    }

    /** Represents a NumericLinesDef. */
    class NumericLinesDef implements INumericLinesDef {

        /**
         * Constructs a new NumericLinesDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.INumericLinesDef);

        /** NumericLinesDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** NumericLinesDef lines. */
        public lines: epoch_proto.INumericLine[];

        /** NumericLinesDef straightLines. */
        public straightLines: epoch_proto.IStraightLineDef[];

        /** NumericLinesDef yPlotBands. */
        public yPlotBands: epoch_proto.IBand[];

        /** NumericLinesDef xPlotBands. */
        public xPlotBands: epoch_proto.IBand[];

        /** NumericLinesDef overlay. */
        public overlay?: (epoch_proto.INumericLine|null);

        /** NumericLinesDef stacked. */
        public stacked: boolean;

        /**
         * Creates a new NumericLinesDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns NumericLinesDef instance
         */
        public static create(properties?: epoch_proto.INumericLinesDef): epoch_proto.NumericLinesDef;

        /**
         * Encodes the specified NumericLinesDef message. Does not implicitly {@link epoch_proto.NumericLinesDef.verify|verify} messages.
         * @param message NumericLinesDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.INumericLinesDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified NumericLinesDef message, length delimited. Does not implicitly {@link epoch_proto.NumericLinesDef.verify|verify} messages.
         * @param message NumericLinesDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.INumericLinesDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a NumericLinesDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns NumericLinesDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.NumericLinesDef;

        /**
         * Decodes a NumericLinesDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns NumericLinesDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.NumericLinesDef;

        /**
         * Verifies a NumericLinesDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a NumericLinesDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns NumericLinesDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.NumericLinesDef;

        /**
         * Creates a plain object from a NumericLinesDef message. Also converts values to other types if specified.
         * @param message NumericLinesDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.NumericLinesDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this NumericLinesDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for NumericLinesDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of an AreaDef. */
    interface IAreaDef {

        /** AreaDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** AreaDef areas */
        areas?: (epoch_proto.ILine[]|null);

        /** AreaDef stacked */
        stacked?: (boolean|null);

        /** AreaDef stackType */
        stackType?: (epoch_proto.StackType|null);
    }

    /** Represents an AreaDef. */
    class AreaDef implements IAreaDef {

        /**
         * Constructs a new AreaDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IAreaDef);

        /** AreaDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** AreaDef areas. */
        public areas: epoch_proto.ILine[];

        /** AreaDef stacked. */
        public stacked: boolean;

        /** AreaDef stackType. */
        public stackType?: (epoch_proto.StackType|null);

        /**
         * Creates a new AreaDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns AreaDef instance
         */
        public static create(properties?: epoch_proto.IAreaDef): epoch_proto.AreaDef;

        /**
         * Encodes the specified AreaDef message. Does not implicitly {@link epoch_proto.AreaDef.verify|verify} messages.
         * @param message AreaDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IAreaDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified AreaDef message, length delimited. Does not implicitly {@link epoch_proto.AreaDef.verify|verify} messages.
         * @param message AreaDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IAreaDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an AreaDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns AreaDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.AreaDef;

        /**
         * Decodes an AreaDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns AreaDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.AreaDef;

        /**
         * Verifies an AreaDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an AreaDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns AreaDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.AreaDef;

        /**
         * Creates a plain object from an AreaDef message. Also converts values to other types if specified.
         * @param message AreaDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.AreaDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this AreaDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for AreaDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BarData. */
    interface IBarData {

        /** BarData name */
        name?: (string|null);

        /** BarData values */
        values?: (number[]|null);

        /** BarData stack */
        stack?: (string|null);
    }

    /** Represents a BarData. */
    class BarData implements IBarData {

        /**
         * Constructs a new BarData.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBarData);

        /** BarData name. */
        public name: string;

        /** BarData values. */
        public values: number[];

        /** BarData stack. */
        public stack?: (string|null);

        /**
         * Creates a new BarData instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BarData instance
         */
        public static create(properties?: epoch_proto.IBarData): epoch_proto.BarData;

        /**
         * Encodes the specified BarData message. Does not implicitly {@link epoch_proto.BarData.verify|verify} messages.
         * @param message BarData message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBarData, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BarData message, length delimited. Does not implicitly {@link epoch_proto.BarData.verify|verify} messages.
         * @param message BarData message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBarData, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BarData message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BarData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BarData;

        /**
         * Decodes a BarData message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BarData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BarData;

        /**
         * Verifies a BarData message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BarData message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BarData
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BarData;

        /**
         * Creates a plain object from a BarData message. Also converts values to other types if specified.
         * @param message BarData
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BarData, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BarData to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BarData
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BarDef. */
    interface IBarDef {

        /** BarDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** BarDef data */
        data?: (epoch_proto.IBarData[]|null);

        /** BarDef straightLines */
        straightLines?: (epoch_proto.IStraightLineDef[]|null);

        /** BarDef barWidth */
        barWidth?: (number|null);

        /** BarDef vertical */
        vertical?: (boolean|null);

        /** BarDef stacked */
        stacked?: (boolean|null);

        /** BarDef stackType */
        stackType?: (epoch_proto.StackType|null);
    }

    /** Represents a BarDef. */
    class BarDef implements IBarDef {

        /**
         * Constructs a new BarDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBarDef);

        /** BarDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** BarDef data. */
        public data: epoch_proto.IBarData[];

        /** BarDef straightLines. */
        public straightLines: epoch_proto.IStraightLineDef[];

        /** BarDef barWidth. */
        public barWidth?: (number|null);

        /** BarDef vertical. */
        public vertical: boolean;

        /** BarDef stacked. */
        public stacked: boolean;

        /** BarDef stackType. */
        public stackType?: (epoch_proto.StackType|null);

        /**
         * Creates a new BarDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BarDef instance
         */
        public static create(properties?: epoch_proto.IBarDef): epoch_proto.BarDef;

        /**
         * Encodes the specified BarDef message. Does not implicitly {@link epoch_proto.BarDef.verify|verify} messages.
         * @param message BarDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBarDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BarDef message, length delimited. Does not implicitly {@link epoch_proto.BarDef.verify|verify} messages.
         * @param message BarDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBarDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BarDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BarDef;

        /**
         * Decodes a BarDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BarDef;

        /**
         * Verifies a BarDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BarDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BarDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BarDef;

        /**
         * Creates a plain object from a BarDef message. Also converts values to other types if specified.
         * @param message BarDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BarDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BarDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BarDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a HeatMapPoint. */
    interface IHeatMapPoint {

        /** HeatMapPoint x */
        x?: (number|Long|null);

        /** HeatMapPoint y */
        y?: (number|Long|null);

        /** HeatMapPoint value */
        value?: (number|null);
    }

    /** Represents a HeatMapPoint. */
    class HeatMapPoint implements IHeatMapPoint {

        /**
         * Constructs a new HeatMapPoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IHeatMapPoint);

        /** HeatMapPoint x. */
        public x: (number|Long);

        /** HeatMapPoint y. */
        public y: (number|Long);

        /** HeatMapPoint value. */
        public value: number;

        /**
         * Creates a new HeatMapPoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns HeatMapPoint instance
         */
        public static create(properties?: epoch_proto.IHeatMapPoint): epoch_proto.HeatMapPoint;

        /**
         * Encodes the specified HeatMapPoint message. Does not implicitly {@link epoch_proto.HeatMapPoint.verify|verify} messages.
         * @param message HeatMapPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IHeatMapPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified HeatMapPoint message, length delimited. Does not implicitly {@link epoch_proto.HeatMapPoint.verify|verify} messages.
         * @param message HeatMapPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IHeatMapPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a HeatMapPoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns HeatMapPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.HeatMapPoint;

        /**
         * Decodes a HeatMapPoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns HeatMapPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.HeatMapPoint;

        /**
         * Verifies a HeatMapPoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a HeatMapPoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns HeatMapPoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.HeatMapPoint;

        /**
         * Creates a plain object from a HeatMapPoint message. Also converts values to other types if specified.
         * @param message HeatMapPoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.HeatMapPoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this HeatMapPoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for HeatMapPoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a HeatMapDef. */
    interface IHeatMapDef {

        /** HeatMapDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** HeatMapDef points */
        points?: (epoch_proto.IHeatMapPoint[]|null);
    }

    /** Represents a HeatMapDef. */
    class HeatMapDef implements IHeatMapDef {

        /**
         * Constructs a new HeatMapDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IHeatMapDef);

        /** HeatMapDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** HeatMapDef points. */
        public points: epoch_proto.IHeatMapPoint[];

        /**
         * Creates a new HeatMapDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns HeatMapDef instance
         */
        public static create(properties?: epoch_proto.IHeatMapDef): epoch_proto.HeatMapDef;

        /**
         * Encodes the specified HeatMapDef message. Does not implicitly {@link epoch_proto.HeatMapDef.verify|verify} messages.
         * @param message HeatMapDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IHeatMapDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified HeatMapDef message, length delimited. Does not implicitly {@link epoch_proto.HeatMapDef.verify|verify} messages.
         * @param message HeatMapDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IHeatMapDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a HeatMapDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns HeatMapDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.HeatMapDef;

        /**
         * Decodes a HeatMapDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns HeatMapDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.HeatMapDef;

        /**
         * Verifies a HeatMapDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a HeatMapDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns HeatMapDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.HeatMapDef;

        /**
         * Creates a plain object from a HeatMapDef message. Also converts values to other types if specified.
         * @param message HeatMapDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.HeatMapDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this HeatMapDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for HeatMapDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a HistogramDef. */
    interface IHistogramDef {

        /** HistogramDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** HistogramDef data */
        data?: (epoch_proto.IArray|null);

        /** HistogramDef straightLines */
        straightLines?: (epoch_proto.IStraightLineDef[]|null);

        /** HistogramDef binsCount */
        binsCount?: (number|null);
    }

    /** Represents a HistogramDef. */
    class HistogramDef implements IHistogramDef {

        /**
         * Constructs a new HistogramDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IHistogramDef);

        /** HistogramDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** HistogramDef data. */
        public data?: (epoch_proto.IArray|null);

        /** HistogramDef straightLines. */
        public straightLines: epoch_proto.IStraightLineDef[];

        /** HistogramDef binsCount. */
        public binsCount?: (number|null);

        /**
         * Creates a new HistogramDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns HistogramDef instance
         */
        public static create(properties?: epoch_proto.IHistogramDef): epoch_proto.HistogramDef;

        /**
         * Encodes the specified HistogramDef message. Does not implicitly {@link epoch_proto.HistogramDef.verify|verify} messages.
         * @param message HistogramDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IHistogramDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified HistogramDef message, length delimited. Does not implicitly {@link epoch_proto.HistogramDef.verify|verify} messages.
         * @param message HistogramDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IHistogramDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a HistogramDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns HistogramDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.HistogramDef;

        /**
         * Decodes a HistogramDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns HistogramDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.HistogramDef;

        /**
         * Verifies a HistogramDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a HistogramDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns HistogramDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.HistogramDef;

        /**
         * Creates a plain object from a HistogramDef message. Also converts values to other types if specified.
         * @param message HistogramDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.HistogramDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this HistogramDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for HistogramDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BoxPlotDataPoint. */
    interface IBoxPlotDataPoint {

        /** BoxPlotDataPoint low */
        low?: (number|null);

        /** BoxPlotDataPoint q1 */
        q1?: (number|null);

        /** BoxPlotDataPoint median */
        median?: (number|null);

        /** BoxPlotDataPoint q3 */
        q3?: (number|null);

        /** BoxPlotDataPoint high */
        high?: (number|null);
    }

    /** Represents a BoxPlotDataPoint. */
    class BoxPlotDataPoint implements IBoxPlotDataPoint {

        /**
         * Constructs a new BoxPlotDataPoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBoxPlotDataPoint);

        /** BoxPlotDataPoint low. */
        public low: number;

        /** BoxPlotDataPoint q1. */
        public q1: number;

        /** BoxPlotDataPoint median. */
        public median: number;

        /** BoxPlotDataPoint q3. */
        public q3: number;

        /** BoxPlotDataPoint high. */
        public high: number;

        /**
         * Creates a new BoxPlotDataPoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BoxPlotDataPoint instance
         */
        public static create(properties?: epoch_proto.IBoxPlotDataPoint): epoch_proto.BoxPlotDataPoint;

        /**
         * Encodes the specified BoxPlotDataPoint message. Does not implicitly {@link epoch_proto.BoxPlotDataPoint.verify|verify} messages.
         * @param message BoxPlotDataPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBoxPlotDataPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BoxPlotDataPoint message, length delimited. Does not implicitly {@link epoch_proto.BoxPlotDataPoint.verify|verify} messages.
         * @param message BoxPlotDataPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBoxPlotDataPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BoxPlotDataPoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BoxPlotDataPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BoxPlotDataPoint;

        /**
         * Decodes a BoxPlotDataPoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BoxPlotDataPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BoxPlotDataPoint;

        /**
         * Verifies a BoxPlotDataPoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BoxPlotDataPoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BoxPlotDataPoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BoxPlotDataPoint;

        /**
         * Creates a plain object from a BoxPlotDataPoint message. Also converts values to other types if specified.
         * @param message BoxPlotDataPoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BoxPlotDataPoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BoxPlotDataPoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BoxPlotDataPoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BoxPlotOutlier. */
    interface IBoxPlotOutlier {

        /** BoxPlotOutlier categoryIndex */
        categoryIndex?: (number|Long|null);

        /** BoxPlotOutlier value */
        value?: (number|null);
    }

    /** Represents a BoxPlotOutlier. */
    class BoxPlotOutlier implements IBoxPlotOutlier {

        /**
         * Constructs a new BoxPlotOutlier.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBoxPlotOutlier);

        /** BoxPlotOutlier categoryIndex. */
        public categoryIndex: (number|Long);

        /** BoxPlotOutlier value. */
        public value: number;

        /**
         * Creates a new BoxPlotOutlier instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BoxPlotOutlier instance
         */
        public static create(properties?: epoch_proto.IBoxPlotOutlier): epoch_proto.BoxPlotOutlier;

        /**
         * Encodes the specified BoxPlotOutlier message. Does not implicitly {@link epoch_proto.BoxPlotOutlier.verify|verify} messages.
         * @param message BoxPlotOutlier message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBoxPlotOutlier, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BoxPlotOutlier message, length delimited. Does not implicitly {@link epoch_proto.BoxPlotOutlier.verify|verify} messages.
         * @param message BoxPlotOutlier message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBoxPlotOutlier, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BoxPlotOutlier message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BoxPlotOutlier
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BoxPlotOutlier;

        /**
         * Decodes a BoxPlotOutlier message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BoxPlotOutlier
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BoxPlotOutlier;

        /**
         * Verifies a BoxPlotOutlier message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BoxPlotOutlier message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BoxPlotOutlier
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BoxPlotOutlier;

        /**
         * Creates a plain object from a BoxPlotOutlier message. Also converts values to other types if specified.
         * @param message BoxPlotOutlier
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BoxPlotOutlier, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BoxPlotOutlier to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BoxPlotOutlier
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BoxPlotDataPointDef. */
    interface IBoxPlotDataPointDef {

        /** BoxPlotDataPointDef outliers */
        outliers?: (epoch_proto.IBoxPlotOutlier[]|null);

        /** BoxPlotDataPointDef points */
        points?: (epoch_proto.IBoxPlotDataPoint[]|null);
    }

    /** Represents a BoxPlotDataPointDef. */
    class BoxPlotDataPointDef implements IBoxPlotDataPointDef {

        /**
         * Constructs a new BoxPlotDataPointDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBoxPlotDataPointDef);

        /** BoxPlotDataPointDef outliers. */
        public outliers: epoch_proto.IBoxPlotOutlier[];

        /** BoxPlotDataPointDef points. */
        public points: epoch_proto.IBoxPlotDataPoint[];

        /**
         * Creates a new BoxPlotDataPointDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BoxPlotDataPointDef instance
         */
        public static create(properties?: epoch_proto.IBoxPlotDataPointDef): epoch_proto.BoxPlotDataPointDef;

        /**
         * Encodes the specified BoxPlotDataPointDef message. Does not implicitly {@link epoch_proto.BoxPlotDataPointDef.verify|verify} messages.
         * @param message BoxPlotDataPointDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBoxPlotDataPointDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BoxPlotDataPointDef message, length delimited. Does not implicitly {@link epoch_proto.BoxPlotDataPointDef.verify|verify} messages.
         * @param message BoxPlotDataPointDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBoxPlotDataPointDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BoxPlotDataPointDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BoxPlotDataPointDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BoxPlotDataPointDef;

        /**
         * Decodes a BoxPlotDataPointDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BoxPlotDataPointDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BoxPlotDataPointDef;

        /**
         * Verifies a BoxPlotDataPointDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BoxPlotDataPointDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BoxPlotDataPointDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BoxPlotDataPointDef;

        /**
         * Creates a plain object from a BoxPlotDataPointDef message. Also converts values to other types if specified.
         * @param message BoxPlotDataPointDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BoxPlotDataPointDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BoxPlotDataPointDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BoxPlotDataPointDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BoxPlotDef. */
    interface IBoxPlotDef {

        /** BoxPlotDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** BoxPlotDef data */
        data?: (epoch_proto.IBoxPlotDataPointDef|null);
    }

    /** Represents a BoxPlotDef. */
    class BoxPlotDef implements IBoxPlotDef {

        /**
         * Constructs a new BoxPlotDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBoxPlotDef);

        /** BoxPlotDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** BoxPlotDef data. */
        public data?: (epoch_proto.IBoxPlotDataPointDef|null);

        /**
         * Creates a new BoxPlotDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BoxPlotDef instance
         */
        public static create(properties?: epoch_proto.IBoxPlotDef): epoch_proto.BoxPlotDef;

        /**
         * Encodes the specified BoxPlotDef message. Does not implicitly {@link epoch_proto.BoxPlotDef.verify|verify} messages.
         * @param message BoxPlotDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBoxPlotDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BoxPlotDef message, length delimited. Does not implicitly {@link epoch_proto.BoxPlotDef.verify|verify} messages.
         * @param message BoxPlotDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBoxPlotDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BoxPlotDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BoxPlotDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BoxPlotDef;

        /**
         * Decodes a BoxPlotDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BoxPlotDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BoxPlotDef;

        /**
         * Verifies a BoxPlotDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BoxPlotDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BoxPlotDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BoxPlotDef;

        /**
         * Creates a plain object from a BoxPlotDef message. Also converts values to other types if specified.
         * @param message BoxPlotDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BoxPlotDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BoxPlotDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BoxPlotDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a XRangePoint. */
    interface IXRangePoint {

        /** XRangePoint x */
        x?: (number|Long|null);

        /** XRangePoint x2 */
        x2?: (number|Long|null);

        /** XRangePoint y */
        y?: (number|Long|null);

        /** XRangePoint isLong */
        isLong?: (boolean|null);
    }

    /** Represents a XRangePoint. */
    class XRangePoint implements IXRangePoint {

        /**
         * Constructs a new XRangePoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IXRangePoint);

        /** XRangePoint x. */
        public x: (number|Long);

        /** XRangePoint x2. */
        public x2: (number|Long);

        /** XRangePoint y. */
        public y: (number|Long);

        /** XRangePoint isLong. */
        public isLong: boolean;

        /**
         * Creates a new XRangePoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns XRangePoint instance
         */
        public static create(properties?: epoch_proto.IXRangePoint): epoch_proto.XRangePoint;

        /**
         * Encodes the specified XRangePoint message. Does not implicitly {@link epoch_proto.XRangePoint.verify|verify} messages.
         * @param message XRangePoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IXRangePoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified XRangePoint message, length delimited. Does not implicitly {@link epoch_proto.XRangePoint.verify|verify} messages.
         * @param message XRangePoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IXRangePoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a XRangePoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns XRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.XRangePoint;

        /**
         * Decodes a XRangePoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns XRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.XRangePoint;

        /**
         * Verifies a XRangePoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a XRangePoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns XRangePoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.XRangePoint;

        /**
         * Creates a plain object from a XRangePoint message. Also converts values to other types if specified.
         * @param message XRangePoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.XRangePoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this XRangePoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for XRangePoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a XRangeDef. */
    interface IXRangeDef {

        /** XRangeDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** XRangeDef categories */
        categories?: (string[]|null);

        /** XRangeDef points */
        points?: (epoch_proto.IXRangePoint[]|null);
    }

    /** Represents a XRangeDef. */
    class XRangeDef implements IXRangeDef {

        /**
         * Constructs a new XRangeDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IXRangeDef);

        /** XRangeDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** XRangeDef categories. */
        public categories: string[];

        /** XRangeDef points. */
        public points: epoch_proto.IXRangePoint[];

        /**
         * Creates a new XRangeDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns XRangeDef instance
         */
        public static create(properties?: epoch_proto.IXRangeDef): epoch_proto.XRangeDef;

        /**
         * Encodes the specified XRangeDef message. Does not implicitly {@link epoch_proto.XRangeDef.verify|verify} messages.
         * @param message XRangeDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IXRangeDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified XRangeDef message, length delimited. Does not implicitly {@link epoch_proto.XRangeDef.verify|verify} messages.
         * @param message XRangeDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IXRangeDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a XRangeDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns XRangeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.XRangeDef;

        /**
         * Decodes a XRangeDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns XRangeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.XRangeDef;

        /**
         * Verifies a XRangeDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a XRangeDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns XRangeDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.XRangeDef;

        /**
         * Creates a plain object from a XRangeDef message. Also converts values to other types if specified.
         * @param message XRangeDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.XRangeDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this XRangeDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for XRangeDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a PieData. */
    interface IPieData {

        /** PieData name */
        name?: (string|null);

        /** PieData y */
        y?: (number|null);
    }

    /** Represents a PieData. */
    class PieData implements IPieData {

        /**
         * Constructs a new PieData.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IPieData);

        /** PieData name. */
        public name: string;

        /** PieData y. */
        public y: number;

        /**
         * Creates a new PieData instance using the specified properties.
         * @param [properties] Properties to set
         * @returns PieData instance
         */
        public static create(properties?: epoch_proto.IPieData): epoch_proto.PieData;

        /**
         * Encodes the specified PieData message. Does not implicitly {@link epoch_proto.PieData.verify|verify} messages.
         * @param message PieData message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IPieData, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified PieData message, length delimited. Does not implicitly {@link epoch_proto.PieData.verify|verify} messages.
         * @param message PieData message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IPieData, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a PieData message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns PieData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.PieData;

        /**
         * Decodes a PieData message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns PieData
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.PieData;

        /**
         * Verifies a PieData message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a PieData message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns PieData
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.PieData;

        /**
         * Creates a plain object from a PieData message. Also converts values to other types if specified.
         * @param message PieData
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.PieData, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this PieData to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for PieData
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a PieDataDef. */
    interface IPieDataDef {

        /** PieDataDef name */
        name?: (string|null);

        /** PieDataDef points */
        points?: (epoch_proto.IPieData[]|null);

        /** PieDataDef size */
        size?: (string|null);

        /** PieDataDef innerSize */
        innerSize?: (string|null);
    }

    /** Represents a PieDataDef. */
    class PieDataDef implements IPieDataDef {

        /**
         * Constructs a new PieDataDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IPieDataDef);

        /** PieDataDef name. */
        public name: string;

        /** PieDataDef points. */
        public points: epoch_proto.IPieData[];

        /** PieDataDef size. */
        public size: string;

        /** PieDataDef innerSize. */
        public innerSize?: (string|null);

        /**
         * Creates a new PieDataDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns PieDataDef instance
         */
        public static create(properties?: epoch_proto.IPieDataDef): epoch_proto.PieDataDef;

        /**
         * Encodes the specified PieDataDef message. Does not implicitly {@link epoch_proto.PieDataDef.verify|verify} messages.
         * @param message PieDataDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IPieDataDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified PieDataDef message, length delimited. Does not implicitly {@link epoch_proto.PieDataDef.verify|verify} messages.
         * @param message PieDataDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IPieDataDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a PieDataDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns PieDataDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.PieDataDef;

        /**
         * Decodes a PieDataDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns PieDataDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.PieDataDef;

        /**
         * Verifies a PieDataDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a PieDataDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns PieDataDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.PieDataDef;

        /**
         * Creates a plain object from a PieDataDef message. Also converts values to other types if specified.
         * @param message PieDataDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.PieDataDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this PieDataDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for PieDataDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a PieDef. */
    interface IPieDef {

        /** PieDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** PieDef data */
        data?: (epoch_proto.IPieDataDef[]|null);
    }

    /** Represents a PieDef. */
    class PieDef implements IPieDef {

        /**
         * Constructs a new PieDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IPieDef);

        /** PieDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** PieDef data. */
        public data: epoch_proto.IPieDataDef[];

        /**
         * Creates a new PieDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns PieDef instance
         */
        public static create(properties?: epoch_proto.IPieDef): epoch_proto.PieDef;

        /**
         * Encodes the specified PieDef message. Does not implicitly {@link epoch_proto.PieDef.verify|verify} messages.
         * @param message PieDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IPieDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified PieDef message, length delimited. Does not implicitly {@link epoch_proto.PieDef.verify|verify} messages.
         * @param message PieDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IPieDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a PieDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns PieDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.PieDef;

        /**
         * Decodes a PieDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns PieDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.PieDef;

        /**
         * Verifies a PieDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a PieDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns PieDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.PieDef;

        /**
         * Creates a plain object from a PieDef message. Also converts values to other types if specified.
         * @param message PieDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.PieDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this PieDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for PieDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a ScatterPoint. */
    interface IScatterPoint {

        /** ScatterPoint x */
        x?: (number|null);

        /** ScatterPoint y */
        y?: (number|null);

        /** ScatterPoint name */
        name?: (string|null);

        /** ScatterPoint color */
        color?: (string|null);
    }

    /** Represents a ScatterPoint. */
    class ScatterPoint implements IScatterPoint {

        /**
         * Constructs a new ScatterPoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IScatterPoint);

        /** ScatterPoint x. */
        public x: number;

        /** ScatterPoint y. */
        public y: number;

        /** ScatterPoint name. */
        public name?: (string|null);

        /** ScatterPoint color. */
        public color?: (string|null);

        /**
         * Creates a new ScatterPoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ScatterPoint instance
         */
        public static create(properties?: epoch_proto.IScatterPoint): epoch_proto.ScatterPoint;

        /**
         * Encodes the specified ScatterPoint message. Does not implicitly {@link epoch_proto.ScatterPoint.verify|verify} messages.
         * @param message ScatterPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IScatterPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ScatterPoint message, length delimited. Does not implicitly {@link epoch_proto.ScatterPoint.verify|verify} messages.
         * @param message ScatterPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IScatterPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a ScatterPoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ScatterPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.ScatterPoint;

        /**
         * Decodes a ScatterPoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ScatterPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.ScatterPoint;

        /**
         * Verifies a ScatterPoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a ScatterPoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ScatterPoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.ScatterPoint;

        /**
         * Creates a plain object from a ScatterPoint message. Also converts values to other types if specified.
         * @param message ScatterPoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.ScatterPoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ScatterPoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for ScatterPoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a ScatterSeries. */
    interface IScatterSeries {

        /** ScatterSeries name */
        name?: (string|null);

        /** ScatterSeries data */
        data?: (epoch_proto.IScatterPoint[]|null);

        /** ScatterSeries color */
        color?: (string|null);
    }

    /** Represents a ScatterSeries. */
    class ScatterSeries implements IScatterSeries {

        /**
         * Constructs a new ScatterSeries.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IScatterSeries);

        /** ScatterSeries name. */
        public name: string;

        /** ScatterSeries data. */
        public data: epoch_proto.IScatterPoint[];

        /** ScatterSeries color. */
        public color?: (string|null);

        /**
         * Creates a new ScatterSeries instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ScatterSeries instance
         */
        public static create(properties?: epoch_proto.IScatterSeries): epoch_proto.ScatterSeries;

        /**
         * Encodes the specified ScatterSeries message. Does not implicitly {@link epoch_proto.ScatterSeries.verify|verify} messages.
         * @param message ScatterSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IScatterSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ScatterSeries message, length delimited. Does not implicitly {@link epoch_proto.ScatterSeries.verify|verify} messages.
         * @param message ScatterSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IScatterSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a ScatterSeries message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ScatterSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.ScatterSeries;

        /**
         * Decodes a ScatterSeries message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ScatterSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.ScatterSeries;

        /**
         * Verifies a ScatterSeries message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a ScatterSeries message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ScatterSeries
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.ScatterSeries;

        /**
         * Creates a plain object from a ScatterSeries message. Also converts values to other types if specified.
         * @param message ScatterSeries
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.ScatterSeries, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ScatterSeries to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for ScatterSeries
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a ScatterDef. */
    interface IScatterDef {

        /** ScatterDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** ScatterDef series */
        series?: (epoch_proto.IScatterSeries[]|null);

        /** ScatterDef straightLines */
        straightLines?: (epoch_proto.IStraightLineDef[]|null);
    }

    /** Represents a ScatterDef. */
    class ScatterDef implements IScatterDef {

        /**
         * Constructs a new ScatterDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IScatterDef);

        /** ScatterDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** ScatterDef series. */
        public series: epoch_proto.IScatterSeries[];

        /** ScatterDef straightLines. */
        public straightLines: epoch_proto.IStraightLineDef[];

        /**
         * Creates a new ScatterDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ScatterDef instance
         */
        public static create(properties?: epoch_proto.IScatterDef): epoch_proto.ScatterDef;

        /**
         * Encodes the specified ScatterDef message. Does not implicitly {@link epoch_proto.ScatterDef.verify|verify} messages.
         * @param message ScatterDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IScatterDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ScatterDef message, length delimited. Does not implicitly {@link epoch_proto.ScatterDef.verify|verify} messages.
         * @param message ScatterDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IScatterDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a ScatterDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ScatterDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.ScatterDef;

        /**
         * Decodes a ScatterDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ScatterDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.ScatterDef;

        /**
         * Verifies a ScatterDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a ScatterDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ScatterDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.ScatterDef;

        /**
         * Creates a plain object from a ScatterDef message. Also converts values to other types if specified.
         * @param message ScatterDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.ScatterDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ScatterDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for ScatterDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a WaterfallPoint. */
    interface IWaterfallPoint {

        /** WaterfallPoint name */
        name?: (string|null);

        /** WaterfallPoint y */
        y?: (number|null);

        /** WaterfallPoint isSum */
        isSum?: (boolean|null);

        /** WaterfallPoint isIntermediateSum */
        isIntermediateSum?: (boolean|null);

        /** WaterfallPoint color */
        color?: (string|null);

        /** WaterfallPoint x */
        x?: (number|Long|null);
    }

    /** Represents a WaterfallPoint. */
    class WaterfallPoint implements IWaterfallPoint {

        /**
         * Constructs a new WaterfallPoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IWaterfallPoint);

        /** WaterfallPoint name. */
        public name: string;

        /** WaterfallPoint y. */
        public y: number;

        /** WaterfallPoint isSum. */
        public isSum: boolean;

        /** WaterfallPoint isIntermediateSum. */
        public isIntermediateSum: boolean;

        /** WaterfallPoint color. */
        public color?: (string|null);

        /** WaterfallPoint x. */
        public x?: (number|Long|null);

        /**
         * Creates a new WaterfallPoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns WaterfallPoint instance
         */
        public static create(properties?: epoch_proto.IWaterfallPoint): epoch_proto.WaterfallPoint;

        /**
         * Encodes the specified WaterfallPoint message. Does not implicitly {@link epoch_proto.WaterfallPoint.verify|verify} messages.
         * @param message WaterfallPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IWaterfallPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified WaterfallPoint message, length delimited. Does not implicitly {@link epoch_proto.WaterfallPoint.verify|verify} messages.
         * @param message WaterfallPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IWaterfallPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a WaterfallPoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns WaterfallPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.WaterfallPoint;

        /**
         * Decodes a WaterfallPoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns WaterfallPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.WaterfallPoint;

        /**
         * Verifies a WaterfallPoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a WaterfallPoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns WaterfallPoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.WaterfallPoint;

        /**
         * Creates a plain object from a WaterfallPoint message. Also converts values to other types if specified.
         * @param message WaterfallPoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.WaterfallPoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this WaterfallPoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for WaterfallPoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a WaterfallDef. */
    interface IWaterfallDef {

        /** WaterfallDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** WaterfallDef points */
        points?: (epoch_proto.IWaterfallPoint[]|null);

        /** WaterfallDef upColor */
        upColor?: (string|null);

        /** WaterfallDef downColor */
        downColor?: (string|null);

        /** WaterfallDef sumColor */
        sumColor?: (string|null);
    }

    /** Represents a WaterfallDef. */
    class WaterfallDef implements IWaterfallDef {

        /**
         * Constructs a new WaterfallDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IWaterfallDef);

        /** WaterfallDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** WaterfallDef points. */
        public points: epoch_proto.IWaterfallPoint[];

        /** WaterfallDef upColor. */
        public upColor?: (string|null);

        /** WaterfallDef downColor. */
        public downColor?: (string|null);

        /** WaterfallDef sumColor. */
        public sumColor?: (string|null);

        /**
         * Creates a new WaterfallDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns WaterfallDef instance
         */
        public static create(properties?: epoch_proto.IWaterfallDef): epoch_proto.WaterfallDef;

        /**
         * Encodes the specified WaterfallDef message. Does not implicitly {@link epoch_proto.WaterfallDef.verify|verify} messages.
         * @param message WaterfallDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IWaterfallDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified WaterfallDef message, length delimited. Does not implicitly {@link epoch_proto.WaterfallDef.verify|verify} messages.
         * @param message WaterfallDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IWaterfallDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a WaterfallDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns WaterfallDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.WaterfallDef;

        /**
         * Decodes a WaterfallDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns WaterfallDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.WaterfallDef;

        /**
         * Verifies a WaterfallDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a WaterfallDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns WaterfallDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.WaterfallDef;

        /**
         * Creates a plain object from a WaterfallDef message. Also converts values to other types if specified.
         * @param message WaterfallDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.WaterfallDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this WaterfallDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for WaterfallDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a SplineDef. */
    interface ISplineDef {

        /** SplineDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** SplineDef lines */
        lines?: (epoch_proto.ILine[]|null);

        /** SplineDef straightLines */
        straightLines?: (epoch_proto.IStraightLineDef[]|null);

        /** SplineDef yPlotBands */
        yPlotBands?: (epoch_proto.IBand[]|null);

        /** SplineDef overlay */
        overlay?: (epoch_proto.ILine|null);
    }

    /** Represents a SplineDef. */
    class SplineDef implements ISplineDef {

        /**
         * Constructs a new SplineDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ISplineDef);

        /** SplineDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** SplineDef lines. */
        public lines: epoch_proto.ILine[];

        /** SplineDef straightLines. */
        public straightLines: epoch_proto.IStraightLineDef[];

        /** SplineDef yPlotBands. */
        public yPlotBands: epoch_proto.IBand[];

        /** SplineDef overlay. */
        public overlay?: (epoch_proto.ILine|null);

        /**
         * Creates a new SplineDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns SplineDef instance
         */
        public static create(properties?: epoch_proto.ISplineDef): epoch_proto.SplineDef;

        /**
         * Encodes the specified SplineDef message. Does not implicitly {@link epoch_proto.SplineDef.verify|verify} messages.
         * @param message SplineDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ISplineDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified SplineDef message, length delimited. Does not implicitly {@link epoch_proto.SplineDef.verify|verify} messages.
         * @param message SplineDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ISplineDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a SplineDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns SplineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.SplineDef;

        /**
         * Decodes a SplineDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns SplineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.SplineDef;

        /**
         * Verifies a SplineDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a SplineDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns SplineDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.SplineDef;

        /**
         * Creates a plain object from a SplineDef message. Also converts values to other types if specified.
         * @param message SplineDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.SplineDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this SplineDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for SplineDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a NumericSplineDef. */
    interface INumericSplineDef {

        /** NumericSplineDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** NumericSplineDef lines */
        lines?: (epoch_proto.INumericLine[]|null);

        /** NumericSplineDef straightLines */
        straightLines?: (epoch_proto.IStraightLineDef[]|null);

        /** NumericSplineDef yPlotBands */
        yPlotBands?: (epoch_proto.IBand[]|null);
    }

    /** Represents a NumericSplineDef. */
    class NumericSplineDef implements INumericSplineDef {

        /**
         * Constructs a new NumericSplineDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.INumericSplineDef);

        /** NumericSplineDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** NumericSplineDef lines. */
        public lines: epoch_proto.INumericLine[];

        /** NumericSplineDef straightLines. */
        public straightLines: epoch_proto.IStraightLineDef[];

        /** NumericSplineDef yPlotBands. */
        public yPlotBands: epoch_proto.IBand[];

        /**
         * Creates a new NumericSplineDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns NumericSplineDef instance
         */
        public static create(properties?: epoch_proto.INumericSplineDef): epoch_proto.NumericSplineDef;

        /**
         * Encodes the specified NumericSplineDef message. Does not implicitly {@link epoch_proto.NumericSplineDef.verify|verify} messages.
         * @param message NumericSplineDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.INumericSplineDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified NumericSplineDef message, length delimited. Does not implicitly {@link epoch_proto.NumericSplineDef.verify|verify} messages.
         * @param message NumericSplineDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.INumericSplineDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a NumericSplineDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns NumericSplineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.NumericSplineDef;

        /**
         * Decodes a NumericSplineDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns NumericSplineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.NumericSplineDef;

        /**
         * Verifies a NumericSplineDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a NumericSplineDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns NumericSplineDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.NumericSplineDef;

        /**
         * Creates a plain object from a NumericSplineDef message. Also converts values to other types if specified.
         * @param message NumericSplineDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.NumericSplineDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this NumericSplineDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for NumericSplineDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BubblePoint. */
    interface IBubblePoint {

        /** BubblePoint x */
        x?: (number|null);

        /** BubblePoint y */
        y?: (number|null);

        /** BubblePoint z */
        z?: (number|null);

        /** BubblePoint name */
        name?: (string|null);

        /** BubblePoint color */
        color?: (string|null);
    }

    /** Represents a BubblePoint. */
    class BubblePoint implements IBubblePoint {

        /**
         * Constructs a new BubblePoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBubblePoint);

        /** BubblePoint x. */
        public x: number;

        /** BubblePoint y. */
        public y: number;

        /** BubblePoint z. */
        public z: number;

        /** BubblePoint name. */
        public name?: (string|null);

        /** BubblePoint color. */
        public color?: (string|null);

        /**
         * Creates a new BubblePoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BubblePoint instance
         */
        public static create(properties?: epoch_proto.IBubblePoint): epoch_proto.BubblePoint;

        /**
         * Encodes the specified BubblePoint message. Does not implicitly {@link epoch_proto.BubblePoint.verify|verify} messages.
         * @param message BubblePoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBubblePoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BubblePoint message, length delimited. Does not implicitly {@link epoch_proto.BubblePoint.verify|verify} messages.
         * @param message BubblePoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBubblePoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BubblePoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BubblePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BubblePoint;

        /**
         * Decodes a BubblePoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BubblePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BubblePoint;

        /**
         * Verifies a BubblePoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BubblePoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BubblePoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BubblePoint;

        /**
         * Creates a plain object from a BubblePoint message. Also converts values to other types if specified.
         * @param message BubblePoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BubblePoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BubblePoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BubblePoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BubbleSeries. */
    interface IBubbleSeries {

        /** BubbleSeries name */
        name?: (string|null);

        /** BubbleSeries data */
        data?: (epoch_proto.IBubblePoint[]|null);
    }

    /** Represents a BubbleSeries. */
    class BubbleSeries implements IBubbleSeries {

        /**
         * Constructs a new BubbleSeries.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBubbleSeries);

        /** BubbleSeries name. */
        public name: string;

        /** BubbleSeries data. */
        public data: epoch_proto.IBubblePoint[];

        /**
         * Creates a new BubbleSeries instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BubbleSeries instance
         */
        public static create(properties?: epoch_proto.IBubbleSeries): epoch_proto.BubbleSeries;

        /**
         * Encodes the specified BubbleSeries message. Does not implicitly {@link epoch_proto.BubbleSeries.verify|verify} messages.
         * @param message BubbleSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBubbleSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BubbleSeries message, length delimited. Does not implicitly {@link epoch_proto.BubbleSeries.verify|verify} messages.
         * @param message BubbleSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBubbleSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BubbleSeries message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BubbleSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BubbleSeries;

        /**
         * Decodes a BubbleSeries message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BubbleSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BubbleSeries;

        /**
         * Verifies a BubbleSeries message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BubbleSeries message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BubbleSeries
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BubbleSeries;

        /**
         * Creates a plain object from a BubbleSeries message. Also converts values to other types if specified.
         * @param message BubbleSeries
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BubbleSeries, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BubbleSeries to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BubbleSeries
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BubbleDef. */
    interface IBubbleDef {

        /** BubbleDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** BubbleDef series */
        series?: (epoch_proto.IBubbleSeries[]|null);

        /** BubbleDef minSize */
        minSize?: (string|null);

        /** BubbleDef maxSize */
        maxSize?: (string|null);

        /** BubbleDef sizeBy */
        sizeBy?: (string|null);
    }

    /** Represents a BubbleDef. */
    class BubbleDef implements IBubbleDef {

        /**
         * Constructs a new BubbleDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBubbleDef);

        /** BubbleDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** BubbleDef series. */
        public series: epoch_proto.IBubbleSeries[];

        /** BubbleDef minSize. */
        public minSize?: (string|null);

        /** BubbleDef maxSize. */
        public maxSize?: (string|null);

        /** BubbleDef sizeBy. */
        public sizeBy?: (string|null);

        /**
         * Creates a new BubbleDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BubbleDef instance
         */
        public static create(properties?: epoch_proto.IBubbleDef): epoch_proto.BubbleDef;

        /**
         * Encodes the specified BubbleDef message. Does not implicitly {@link epoch_proto.BubbleDef.verify|verify} messages.
         * @param message BubbleDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBubbleDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BubbleDef message, length delimited. Does not implicitly {@link epoch_proto.BubbleDef.verify|verify} messages.
         * @param message BubbleDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBubbleDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BubbleDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BubbleDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BubbleDef;

        /**
         * Decodes a BubbleDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BubbleDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BubbleDef;

        /**
         * Verifies a BubbleDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BubbleDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BubbleDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BubbleDef;

        /**
         * Creates a plain object from a BubbleDef message. Also converts values to other types if specified.
         * @param message BubbleDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BubbleDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BubbleDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BubbleDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a TreemapPoint. */
    interface ITreemapPoint {

        /** TreemapPoint id */
        id?: (string|null);

        /** TreemapPoint parent */
        parent?: (string|null);

        /** TreemapPoint name */
        name?: (string|null);

        /** TreemapPoint value */
        value?: (number|null);

        /** TreemapPoint color */
        color?: (string|null);

        /** TreemapPoint colorValue */
        colorValue?: (number|null);
    }

    /** Represents a TreemapPoint. */
    class TreemapPoint implements ITreemapPoint {

        /**
         * Constructs a new TreemapPoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ITreemapPoint);

        /** TreemapPoint id. */
        public id: string;

        /** TreemapPoint parent. */
        public parent?: (string|null);

        /** TreemapPoint name. */
        public name: string;

        /** TreemapPoint value. */
        public value?: (number|null);

        /** TreemapPoint color. */
        public color?: (string|null);

        /** TreemapPoint colorValue. */
        public colorValue?: (number|null);

        /**
         * Creates a new TreemapPoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns TreemapPoint instance
         */
        public static create(properties?: epoch_proto.ITreemapPoint): epoch_proto.TreemapPoint;

        /**
         * Encodes the specified TreemapPoint message. Does not implicitly {@link epoch_proto.TreemapPoint.verify|verify} messages.
         * @param message TreemapPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ITreemapPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified TreemapPoint message, length delimited. Does not implicitly {@link epoch_proto.TreemapPoint.verify|verify} messages.
         * @param message TreemapPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ITreemapPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a TreemapPoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns TreemapPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.TreemapPoint;

        /**
         * Decodes a TreemapPoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns TreemapPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.TreemapPoint;

        /**
         * Verifies a TreemapPoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a TreemapPoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns TreemapPoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.TreemapPoint;

        /**
         * Creates a plain object from a TreemapPoint message. Also converts values to other types if specified.
         * @param message TreemapPoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.TreemapPoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this TreemapPoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for TreemapPoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a TreemapDef. */
    interface ITreemapDef {

        /** TreemapDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** TreemapDef points */
        points?: (epoch_proto.ITreemapPoint[]|null);

        /** TreemapDef layoutAlgorithm */
        layoutAlgorithm?: (string|null);
    }

    /** Represents a TreemapDef. */
    class TreemapDef implements ITreemapDef {

        /**
         * Constructs a new TreemapDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ITreemapDef);

        /** TreemapDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** TreemapDef points. */
        public points: epoch_proto.ITreemapPoint[];

        /** TreemapDef layoutAlgorithm. */
        public layoutAlgorithm?: (string|null);

        /**
         * Creates a new TreemapDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns TreemapDef instance
         */
        public static create(properties?: epoch_proto.ITreemapDef): epoch_proto.TreemapDef;

        /**
         * Encodes the specified TreemapDef message. Does not implicitly {@link epoch_proto.TreemapDef.verify|verify} messages.
         * @param message TreemapDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ITreemapDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified TreemapDef message, length delimited. Does not implicitly {@link epoch_proto.TreemapDef.verify|verify} messages.
         * @param message TreemapDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ITreemapDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a TreemapDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns TreemapDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.TreemapDef;

        /**
         * Decodes a TreemapDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns TreemapDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.TreemapDef;

        /**
         * Verifies a TreemapDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a TreemapDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns TreemapDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.TreemapDef;

        /**
         * Creates a plain object from a TreemapDef message. Also converts values to other types if specified.
         * @param message TreemapDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.TreemapDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this TreemapDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for TreemapDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a SankeyLink. */
    interface ISankeyLink {

        /** SankeyLink from */
        from?: (string|null);

        /** SankeyLink to */
        to?: (string|null);

        /** SankeyLink weight */
        weight?: (number|null);

        /** SankeyLink color */
        color?: (string|null);
    }

    /** Represents a SankeyLink. */
    class SankeyLink implements ISankeyLink {

        /**
         * Constructs a new SankeyLink.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ISankeyLink);

        /** SankeyLink from. */
        public from: string;

        /** SankeyLink to. */
        public to: string;

        /** SankeyLink weight. */
        public weight: number;

        /** SankeyLink color. */
        public color?: (string|null);

        /**
         * Creates a new SankeyLink instance using the specified properties.
         * @param [properties] Properties to set
         * @returns SankeyLink instance
         */
        public static create(properties?: epoch_proto.ISankeyLink): epoch_proto.SankeyLink;

        /**
         * Encodes the specified SankeyLink message. Does not implicitly {@link epoch_proto.SankeyLink.verify|verify} messages.
         * @param message SankeyLink message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ISankeyLink, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified SankeyLink message, length delimited. Does not implicitly {@link epoch_proto.SankeyLink.verify|verify} messages.
         * @param message SankeyLink message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ISankeyLink, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a SankeyLink message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns SankeyLink
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.SankeyLink;

        /**
         * Decodes a SankeyLink message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns SankeyLink
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.SankeyLink;

        /**
         * Verifies a SankeyLink message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a SankeyLink message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns SankeyLink
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.SankeyLink;

        /**
         * Creates a plain object from a SankeyLink message. Also converts values to other types if specified.
         * @param message SankeyLink
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.SankeyLink, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this SankeyLink to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for SankeyLink
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a SankeyNode. */
    interface ISankeyNode {

        /** SankeyNode id */
        id?: (string|null);

        /** SankeyNode name */
        name?: (string|null);

        /** SankeyNode color */
        color?: (string|null);
    }

    /** Represents a SankeyNode. */
    class SankeyNode implements ISankeyNode {

        /**
         * Constructs a new SankeyNode.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ISankeyNode);

        /** SankeyNode id. */
        public id: string;

        /** SankeyNode name. */
        public name?: (string|null);

        /** SankeyNode color. */
        public color?: (string|null);

        /**
         * Creates a new SankeyNode instance using the specified properties.
         * @param [properties] Properties to set
         * @returns SankeyNode instance
         */
        public static create(properties?: epoch_proto.ISankeyNode): epoch_proto.SankeyNode;

        /**
         * Encodes the specified SankeyNode message. Does not implicitly {@link epoch_proto.SankeyNode.verify|verify} messages.
         * @param message SankeyNode message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ISankeyNode, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified SankeyNode message, length delimited. Does not implicitly {@link epoch_proto.SankeyNode.verify|verify} messages.
         * @param message SankeyNode message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ISankeyNode, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a SankeyNode message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns SankeyNode
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.SankeyNode;

        /**
         * Decodes a SankeyNode message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns SankeyNode
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.SankeyNode;

        /**
         * Verifies a SankeyNode message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a SankeyNode message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns SankeyNode
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.SankeyNode;

        /**
         * Creates a plain object from a SankeyNode message. Also converts values to other types if specified.
         * @param message SankeyNode
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.SankeyNode, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this SankeyNode to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for SankeyNode
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a SankeyDef. */
    interface ISankeyDef {

        /** SankeyDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** SankeyDef links */
        links?: (epoch_proto.ISankeyLink[]|null);

        /** SankeyDef nodes */
        nodes?: (epoch_proto.ISankeyNode[]|null);

        /** SankeyDef curveFactor */
        curveFactor?: (number|null);
    }

    /** Represents a SankeyDef. */
    class SankeyDef implements ISankeyDef {

        /**
         * Constructs a new SankeyDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ISankeyDef);

        /** SankeyDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** SankeyDef links. */
        public links: epoch_proto.ISankeyLink[];

        /** SankeyDef nodes. */
        public nodes: epoch_proto.ISankeyNode[];

        /** SankeyDef curveFactor. */
        public curveFactor?: (number|null);

        /**
         * Creates a new SankeyDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns SankeyDef instance
         */
        public static create(properties?: epoch_proto.ISankeyDef): epoch_proto.SankeyDef;

        /**
         * Encodes the specified SankeyDef message. Does not implicitly {@link epoch_proto.SankeyDef.verify|verify} messages.
         * @param message SankeyDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ISankeyDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified SankeyDef message, length delimited. Does not implicitly {@link epoch_proto.SankeyDef.verify|verify} messages.
         * @param message SankeyDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ISankeyDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a SankeyDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns SankeyDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.SankeyDef;

        /**
         * Decodes a SankeyDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns SankeyDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.SankeyDef;

        /**
         * Verifies a SankeyDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a SankeyDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns SankeyDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.SankeyDef;

        /**
         * Creates a plain object from a SankeyDef message. Also converts values to other types if specified.
         * @param message SankeyDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.SankeyDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this SankeyDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for SankeyDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of an AreaRangePoint. */
    interface IAreaRangePoint {

        /** AreaRangePoint x */
        x?: (number|Long|null);

        /** AreaRangePoint low */
        low?: (number|null);

        /** AreaRangePoint high */
        high?: (number|null);
    }

    /** Represents an AreaRangePoint. */
    class AreaRangePoint implements IAreaRangePoint {

        /**
         * Constructs a new AreaRangePoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IAreaRangePoint);

        /** AreaRangePoint x. */
        public x: (number|Long);

        /** AreaRangePoint low. */
        public low: number;

        /** AreaRangePoint high. */
        public high: number;

        /**
         * Creates a new AreaRangePoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns AreaRangePoint instance
         */
        public static create(properties?: epoch_proto.IAreaRangePoint): epoch_proto.AreaRangePoint;

        /**
         * Encodes the specified AreaRangePoint message. Does not implicitly {@link epoch_proto.AreaRangePoint.verify|verify} messages.
         * @param message AreaRangePoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IAreaRangePoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified AreaRangePoint message, length delimited. Does not implicitly {@link epoch_proto.AreaRangePoint.verify|verify} messages.
         * @param message AreaRangePoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IAreaRangePoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an AreaRangePoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns AreaRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.AreaRangePoint;

        /**
         * Decodes an AreaRangePoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns AreaRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.AreaRangePoint;

        /**
         * Verifies an AreaRangePoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an AreaRangePoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns AreaRangePoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.AreaRangePoint;

        /**
         * Creates a plain object from an AreaRangePoint message. Also converts values to other types if specified.
         * @param message AreaRangePoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.AreaRangePoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this AreaRangePoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for AreaRangePoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a NumericAreaRangePoint. */
    interface INumericAreaRangePoint {

        /** NumericAreaRangePoint x */
        x?: (number|null);

        /** NumericAreaRangePoint low */
        low?: (number|null);

        /** NumericAreaRangePoint high */
        high?: (number|null);
    }

    /** Represents a NumericAreaRangePoint. */
    class NumericAreaRangePoint implements INumericAreaRangePoint {

        /**
         * Constructs a new NumericAreaRangePoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.INumericAreaRangePoint);

        /** NumericAreaRangePoint x. */
        public x: number;

        /** NumericAreaRangePoint low. */
        public low: number;

        /** NumericAreaRangePoint high. */
        public high: number;

        /**
         * Creates a new NumericAreaRangePoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns NumericAreaRangePoint instance
         */
        public static create(properties?: epoch_proto.INumericAreaRangePoint): epoch_proto.NumericAreaRangePoint;

        /**
         * Encodes the specified NumericAreaRangePoint message. Does not implicitly {@link epoch_proto.NumericAreaRangePoint.verify|verify} messages.
         * @param message NumericAreaRangePoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.INumericAreaRangePoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified NumericAreaRangePoint message, length delimited. Does not implicitly {@link epoch_proto.NumericAreaRangePoint.verify|verify} messages.
         * @param message NumericAreaRangePoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.INumericAreaRangePoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a NumericAreaRangePoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns NumericAreaRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.NumericAreaRangePoint;

        /**
         * Decodes a NumericAreaRangePoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns NumericAreaRangePoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.NumericAreaRangePoint;

        /**
         * Verifies a NumericAreaRangePoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a NumericAreaRangePoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns NumericAreaRangePoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.NumericAreaRangePoint;

        /**
         * Creates a plain object from a NumericAreaRangePoint message. Also converts values to other types if specified.
         * @param message NumericAreaRangePoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.NumericAreaRangePoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this NumericAreaRangePoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for NumericAreaRangePoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of an AreaRangeSeries. */
    interface IAreaRangeSeries {

        /** AreaRangeSeries name */
        name?: (string|null);

        /** AreaRangeSeries data */
        data?: (epoch_proto.IAreaRangePoint[]|null);

        /** AreaRangeSeries fillColor */
        fillColor?: (string|null);

        /** AreaRangeSeries fillOpacity */
        fillOpacity?: (number|null);
    }

    /** Represents an AreaRangeSeries. */
    class AreaRangeSeries implements IAreaRangeSeries {

        /**
         * Constructs a new AreaRangeSeries.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IAreaRangeSeries);

        /** AreaRangeSeries name. */
        public name: string;

        /** AreaRangeSeries data. */
        public data: epoch_proto.IAreaRangePoint[];

        /** AreaRangeSeries fillColor. */
        public fillColor?: (string|null);

        /** AreaRangeSeries fillOpacity. */
        public fillOpacity?: (number|null);

        /**
         * Creates a new AreaRangeSeries instance using the specified properties.
         * @param [properties] Properties to set
         * @returns AreaRangeSeries instance
         */
        public static create(properties?: epoch_proto.IAreaRangeSeries): epoch_proto.AreaRangeSeries;

        /**
         * Encodes the specified AreaRangeSeries message. Does not implicitly {@link epoch_proto.AreaRangeSeries.verify|verify} messages.
         * @param message AreaRangeSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IAreaRangeSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified AreaRangeSeries message, length delimited. Does not implicitly {@link epoch_proto.AreaRangeSeries.verify|verify} messages.
         * @param message AreaRangeSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IAreaRangeSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an AreaRangeSeries message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns AreaRangeSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.AreaRangeSeries;

        /**
         * Decodes an AreaRangeSeries message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns AreaRangeSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.AreaRangeSeries;

        /**
         * Verifies an AreaRangeSeries message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an AreaRangeSeries message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns AreaRangeSeries
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.AreaRangeSeries;

        /**
         * Creates a plain object from an AreaRangeSeries message. Also converts values to other types if specified.
         * @param message AreaRangeSeries
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.AreaRangeSeries, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this AreaRangeSeries to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for AreaRangeSeries
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of an AreaRangeDef. */
    interface IAreaRangeDef {

        /** AreaRangeDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** AreaRangeDef series */
        series?: (epoch_proto.IAreaRangeSeries[]|null);

        /** AreaRangeDef centerLine */
        centerLine?: (epoch_proto.ILine|null);
    }

    /** Represents an AreaRangeDef. */
    class AreaRangeDef implements IAreaRangeDef {

        /**
         * Constructs a new AreaRangeDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IAreaRangeDef);

        /** AreaRangeDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** AreaRangeDef series. */
        public series: epoch_proto.IAreaRangeSeries[];

        /** AreaRangeDef centerLine. */
        public centerLine?: (epoch_proto.ILine|null);

        /**
         * Creates a new AreaRangeDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns AreaRangeDef instance
         */
        public static create(properties?: epoch_proto.IAreaRangeDef): epoch_proto.AreaRangeDef;

        /**
         * Encodes the specified AreaRangeDef message. Does not implicitly {@link epoch_proto.AreaRangeDef.verify|verify} messages.
         * @param message AreaRangeDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IAreaRangeDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified AreaRangeDef message, length delimited. Does not implicitly {@link epoch_proto.AreaRangeDef.verify|verify} messages.
         * @param message AreaRangeDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IAreaRangeDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an AreaRangeDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns AreaRangeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.AreaRangeDef;

        /**
         * Decodes an AreaRangeDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns AreaRangeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.AreaRangeDef;

        /**
         * Verifies an AreaRangeDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an AreaRangeDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns AreaRangeDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.AreaRangeDef;

        /**
         * Creates a plain object from an AreaRangeDef message. Also converts values to other types if specified.
         * @param message AreaRangeDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.AreaRangeDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this AreaRangeDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for AreaRangeDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a GaugeStop. */
    interface IGaugeStop {

        /** GaugeStop position */
        position?: (number|null);

        /** GaugeStop color */
        color?: (string|null);
    }

    /** Represents a GaugeStop. */
    class GaugeStop implements IGaugeStop {

        /**
         * Constructs a new GaugeStop.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IGaugeStop);

        /** GaugeStop position. */
        public position: number;

        /** GaugeStop color. */
        public color: string;

        /**
         * Creates a new GaugeStop instance using the specified properties.
         * @param [properties] Properties to set
         * @returns GaugeStop instance
         */
        public static create(properties?: epoch_proto.IGaugeStop): epoch_proto.GaugeStop;

        /**
         * Encodes the specified GaugeStop message. Does not implicitly {@link epoch_proto.GaugeStop.verify|verify} messages.
         * @param message GaugeStop message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IGaugeStop, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified GaugeStop message, length delimited. Does not implicitly {@link epoch_proto.GaugeStop.verify|verify} messages.
         * @param message GaugeStop message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IGaugeStop, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a GaugeStop message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns GaugeStop
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.GaugeStop;

        /**
         * Decodes a GaugeStop message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns GaugeStop
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.GaugeStop;

        /**
         * Verifies a GaugeStop message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a GaugeStop message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns GaugeStop
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.GaugeStop;

        /**
         * Creates a plain object from a GaugeStop message. Also converts values to other types if specified.
         * @param message GaugeStop
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.GaugeStop, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this GaugeStop to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for GaugeStop
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a GaugeDef. */
    interface IGaugeDef {

        /** GaugeDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** GaugeDef value */
        value?: (number|null);

        /** GaugeDef min */
        min?: (number|null);

        /** GaugeDef max */
        max?: (number|null);

        /** GaugeDef valueSuffix */
        valueSuffix?: (string|null);

        /** GaugeDef stops */
        stops?: (epoch_proto.IGaugeStop[]|null);

        /** GaugeDef solid */
        solid?: (boolean|null);
    }

    /** Represents a GaugeDef. */
    class GaugeDef implements IGaugeDef {

        /**
         * Constructs a new GaugeDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IGaugeDef);

        /** GaugeDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** GaugeDef value. */
        public value: number;

        /** GaugeDef min. */
        public min: number;

        /** GaugeDef max. */
        public max: number;

        /** GaugeDef valueSuffix. */
        public valueSuffix?: (string|null);

        /** GaugeDef stops. */
        public stops: epoch_proto.IGaugeStop[];

        /** GaugeDef solid. */
        public solid: boolean;

        /**
         * Creates a new GaugeDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns GaugeDef instance
         */
        public static create(properties?: epoch_proto.IGaugeDef): epoch_proto.GaugeDef;

        /**
         * Encodes the specified GaugeDef message. Does not implicitly {@link epoch_proto.GaugeDef.verify|verify} messages.
         * @param message GaugeDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IGaugeDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified GaugeDef message, length delimited. Does not implicitly {@link epoch_proto.GaugeDef.verify|verify} messages.
         * @param message GaugeDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IGaugeDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a GaugeDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns GaugeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.GaugeDef;

        /**
         * Decodes a GaugeDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns GaugeDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.GaugeDef;

        /**
         * Verifies a GaugeDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a GaugeDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns GaugeDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.GaugeDef;

        /**
         * Creates a plain object from a GaugeDef message. Also converts values to other types if specified.
         * @param message GaugeDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.GaugeDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this GaugeDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for GaugeDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BulletRange. */
    interface IBulletRange {

        /** BulletRange from */
        from?: (number|null);

        /** BulletRange to */
        to?: (number|null);

        /** BulletRange color */
        color?: (string|null);
    }

    /** Represents a BulletRange. */
    class BulletRange implements IBulletRange {

        /**
         * Constructs a new BulletRange.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBulletRange);

        /** BulletRange from. */
        public from: number;

        /** BulletRange to. */
        public to: number;

        /** BulletRange color. */
        public color: string;

        /**
         * Creates a new BulletRange instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BulletRange instance
         */
        public static create(properties?: epoch_proto.IBulletRange): epoch_proto.BulletRange;

        /**
         * Encodes the specified BulletRange message. Does not implicitly {@link epoch_proto.BulletRange.verify|verify} messages.
         * @param message BulletRange message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBulletRange, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BulletRange message, length delimited. Does not implicitly {@link epoch_proto.BulletRange.verify|verify} messages.
         * @param message BulletRange message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBulletRange, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BulletRange message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BulletRange
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BulletRange;

        /**
         * Decodes a BulletRange message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BulletRange
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BulletRange;

        /**
         * Verifies a BulletRange message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BulletRange message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BulletRange
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BulletRange;

        /**
         * Creates a plain object from a BulletRange message. Also converts values to other types if specified.
         * @param message BulletRange
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BulletRange, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BulletRange to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BulletRange
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BulletDef. */
    interface IBulletDef {

        /** BulletDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** BulletDef value */
        value?: (number|null);

        /** BulletDef target */
        target?: (number|null);

        /** BulletDef ranges */
        ranges?: (epoch_proto.IBulletRange[]|null);
    }

    /** Represents a BulletDef. */
    class BulletDef implements IBulletDef {

        /**
         * Constructs a new BulletDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBulletDef);

        /** BulletDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** BulletDef value. */
        public value: number;

        /** BulletDef target. */
        public target: number;

        /** BulletDef ranges. */
        public ranges: epoch_proto.IBulletRange[];

        /**
         * Creates a new BulletDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BulletDef instance
         */
        public static create(properties?: epoch_proto.IBulletDef): epoch_proto.BulletDef;

        /**
         * Encodes the specified BulletDef message. Does not implicitly {@link epoch_proto.BulletDef.verify|verify} messages.
         * @param message BulletDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBulletDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BulletDef message, length delimited. Does not implicitly {@link epoch_proto.BulletDef.verify|verify} messages.
         * @param message BulletDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBulletDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BulletDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BulletDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BulletDef;

        /**
         * Decodes a BulletDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BulletDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BulletDef;

        /**
         * Verifies a BulletDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BulletDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BulletDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BulletDef;

        /**
         * Creates a plain object from a BulletDef message. Also converts values to other types if specified.
         * @param message BulletDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BulletDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BulletDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BulletDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a TimelineEvent. */
    interface ITimelineEvent {

        /** TimelineEvent timestamp */
        timestamp?: (number|Long|null);

        /** TimelineEvent name */
        name?: (string|null);

        /** TimelineEvent label */
        label?: (string|null);

        /** TimelineEvent description */
        description?: (string|null);

        /** TimelineEvent color */
        color?: (string|null);
    }

    /** Represents a TimelineEvent. */
    class TimelineEvent implements ITimelineEvent {

        /**
         * Constructs a new TimelineEvent.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ITimelineEvent);

        /** TimelineEvent timestamp. */
        public timestamp: (number|Long);

        /** TimelineEvent name. */
        public name: string;

        /** TimelineEvent label. */
        public label?: (string|null);

        /** TimelineEvent description. */
        public description?: (string|null);

        /** TimelineEvent color. */
        public color?: (string|null);

        /**
         * Creates a new TimelineEvent instance using the specified properties.
         * @param [properties] Properties to set
         * @returns TimelineEvent instance
         */
        public static create(properties?: epoch_proto.ITimelineEvent): epoch_proto.TimelineEvent;

        /**
         * Encodes the specified TimelineEvent message. Does not implicitly {@link epoch_proto.TimelineEvent.verify|verify} messages.
         * @param message TimelineEvent message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ITimelineEvent, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified TimelineEvent message, length delimited. Does not implicitly {@link epoch_proto.TimelineEvent.verify|verify} messages.
         * @param message TimelineEvent message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ITimelineEvent, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a TimelineEvent message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns TimelineEvent
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.TimelineEvent;

        /**
         * Decodes a TimelineEvent message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns TimelineEvent
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.TimelineEvent;

        /**
         * Verifies a TimelineEvent message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a TimelineEvent message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns TimelineEvent
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.TimelineEvent;

        /**
         * Creates a plain object from a TimelineEvent message. Also converts values to other types if specified.
         * @param message TimelineEvent
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.TimelineEvent, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this TimelineEvent to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for TimelineEvent
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a TimelineDef. */
    interface ITimelineDef {

        /** TimelineDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** TimelineDef events */
        events?: (epoch_proto.ITimelineEvent[]|null);
    }

    /** Represents a TimelineDef. */
    class TimelineDef implements ITimelineDef {

        /**
         * Constructs a new TimelineDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ITimelineDef);

        /** TimelineDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** TimelineDef events. */
        public events: epoch_proto.ITimelineEvent[];

        /**
         * Creates a new TimelineDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns TimelineDef instance
         */
        public static create(properties?: epoch_proto.ITimelineDef): epoch_proto.TimelineDef;

        /**
         * Encodes the specified TimelineDef message. Does not implicitly {@link epoch_proto.TimelineDef.verify|verify} messages.
         * @param message TimelineDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ITimelineDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified TimelineDef message, length delimited. Does not implicitly {@link epoch_proto.TimelineDef.verify|verify} messages.
         * @param message TimelineDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ITimelineDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a TimelineDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns TimelineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.TimelineDef;

        /**
         * Decodes a TimelineDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns TimelineDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.TimelineDef;

        /**
         * Verifies a TimelineDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a TimelineDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns TimelineDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.TimelineDef;

        /**
         * Creates a plain object from a TimelineDef message. Also converts values to other types if specified.
         * @param message TimelineDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.TimelineDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this TimelineDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for TimelineDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of an ErrorBarPoint. */
    interface IErrorBarPoint {

        /** ErrorBarPoint x */
        x?: (number|Long|null);

        /** ErrorBarPoint low */
        low?: (number|null);

        /** ErrorBarPoint high */
        high?: (number|null);
    }

    /** Represents an ErrorBarPoint. */
    class ErrorBarPoint implements IErrorBarPoint {

        /**
         * Constructs a new ErrorBarPoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IErrorBarPoint);

        /** ErrorBarPoint x. */
        public x: (number|Long);

        /** ErrorBarPoint low. */
        public low: number;

        /** ErrorBarPoint high. */
        public high: number;

        /**
         * Creates a new ErrorBarPoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ErrorBarPoint instance
         */
        public static create(properties?: epoch_proto.IErrorBarPoint): epoch_proto.ErrorBarPoint;

        /**
         * Encodes the specified ErrorBarPoint message. Does not implicitly {@link epoch_proto.ErrorBarPoint.verify|verify} messages.
         * @param message ErrorBarPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IErrorBarPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ErrorBarPoint message, length delimited. Does not implicitly {@link epoch_proto.ErrorBarPoint.verify|verify} messages.
         * @param message ErrorBarPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IErrorBarPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an ErrorBarPoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ErrorBarPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.ErrorBarPoint;

        /**
         * Decodes an ErrorBarPoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ErrorBarPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.ErrorBarPoint;

        /**
         * Verifies an ErrorBarPoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an ErrorBarPoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ErrorBarPoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.ErrorBarPoint;

        /**
         * Creates a plain object from an ErrorBarPoint message. Also converts values to other types if specified.
         * @param message ErrorBarPoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.ErrorBarPoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ErrorBarPoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for ErrorBarPoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a NumericErrorBarPoint. */
    interface INumericErrorBarPoint {

        /** NumericErrorBarPoint x */
        x?: (number|null);

        /** NumericErrorBarPoint low */
        low?: (number|null);

        /** NumericErrorBarPoint high */
        high?: (number|null);
    }

    /** Represents a NumericErrorBarPoint. */
    class NumericErrorBarPoint implements INumericErrorBarPoint {

        /**
         * Constructs a new NumericErrorBarPoint.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.INumericErrorBarPoint);

        /** NumericErrorBarPoint x. */
        public x: number;

        /** NumericErrorBarPoint low. */
        public low: number;

        /** NumericErrorBarPoint high. */
        public high: number;

        /**
         * Creates a new NumericErrorBarPoint instance using the specified properties.
         * @param [properties] Properties to set
         * @returns NumericErrorBarPoint instance
         */
        public static create(properties?: epoch_proto.INumericErrorBarPoint): epoch_proto.NumericErrorBarPoint;

        /**
         * Encodes the specified NumericErrorBarPoint message. Does not implicitly {@link epoch_proto.NumericErrorBarPoint.verify|verify} messages.
         * @param message NumericErrorBarPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.INumericErrorBarPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified NumericErrorBarPoint message, length delimited. Does not implicitly {@link epoch_proto.NumericErrorBarPoint.verify|verify} messages.
         * @param message NumericErrorBarPoint message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.INumericErrorBarPoint, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a NumericErrorBarPoint message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns NumericErrorBarPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.NumericErrorBarPoint;

        /**
         * Decodes a NumericErrorBarPoint message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns NumericErrorBarPoint
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.NumericErrorBarPoint;

        /**
         * Verifies a NumericErrorBarPoint message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a NumericErrorBarPoint message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns NumericErrorBarPoint
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.NumericErrorBarPoint;

        /**
         * Creates a plain object from a NumericErrorBarPoint message. Also converts values to other types if specified.
         * @param message NumericErrorBarPoint
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.NumericErrorBarPoint, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this NumericErrorBarPoint to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for NumericErrorBarPoint
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of an ErrorBarSeries. */
    interface IErrorBarSeries {

        /** ErrorBarSeries name */
        name?: (string|null);

        /** ErrorBarSeries data */
        data?: (epoch_proto.IErrorBarPoint[]|null);

        /** ErrorBarSeries whiskerColor */
        whiskerColor?: (string|null);

        /** ErrorBarSeries whiskerWidth */
        whiskerWidth?: (number|null);
    }

    /** Represents an ErrorBarSeries. */
    class ErrorBarSeries implements IErrorBarSeries {

        /**
         * Constructs a new ErrorBarSeries.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IErrorBarSeries);

        /** ErrorBarSeries name. */
        public name: string;

        /** ErrorBarSeries data. */
        public data: epoch_proto.IErrorBarPoint[];

        /** ErrorBarSeries whiskerColor. */
        public whiskerColor?: (string|null);

        /** ErrorBarSeries whiskerWidth. */
        public whiskerWidth?: (number|null);

        /**
         * Creates a new ErrorBarSeries instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ErrorBarSeries instance
         */
        public static create(properties?: epoch_proto.IErrorBarSeries): epoch_proto.ErrorBarSeries;

        /**
         * Encodes the specified ErrorBarSeries message. Does not implicitly {@link epoch_proto.ErrorBarSeries.verify|verify} messages.
         * @param message ErrorBarSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IErrorBarSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ErrorBarSeries message, length delimited. Does not implicitly {@link epoch_proto.ErrorBarSeries.verify|verify} messages.
         * @param message ErrorBarSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IErrorBarSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an ErrorBarSeries message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ErrorBarSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.ErrorBarSeries;

        /**
         * Decodes an ErrorBarSeries message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ErrorBarSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.ErrorBarSeries;

        /**
         * Verifies an ErrorBarSeries message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an ErrorBarSeries message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ErrorBarSeries
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.ErrorBarSeries;

        /**
         * Creates a plain object from an ErrorBarSeries message. Also converts values to other types if specified.
         * @param message ErrorBarSeries
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.ErrorBarSeries, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ErrorBarSeries to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for ErrorBarSeries
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a NumericErrorBarSeries. */
    interface INumericErrorBarSeries {

        /** NumericErrorBarSeries name */
        name?: (string|null);

        /** NumericErrorBarSeries data */
        data?: (epoch_proto.INumericErrorBarPoint[]|null);

        /** NumericErrorBarSeries whiskerColor */
        whiskerColor?: (string|null);

        /** NumericErrorBarSeries whiskerWidth */
        whiskerWidth?: (number|null);
    }

    /** Represents a NumericErrorBarSeries. */
    class NumericErrorBarSeries implements INumericErrorBarSeries {

        /**
         * Constructs a new NumericErrorBarSeries.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.INumericErrorBarSeries);

        /** NumericErrorBarSeries name. */
        public name: string;

        /** NumericErrorBarSeries data. */
        public data: epoch_proto.INumericErrorBarPoint[];

        /** NumericErrorBarSeries whiskerColor. */
        public whiskerColor?: (string|null);

        /** NumericErrorBarSeries whiskerWidth. */
        public whiskerWidth?: (number|null);

        /**
         * Creates a new NumericErrorBarSeries instance using the specified properties.
         * @param [properties] Properties to set
         * @returns NumericErrorBarSeries instance
         */
        public static create(properties?: epoch_proto.INumericErrorBarSeries): epoch_proto.NumericErrorBarSeries;

        /**
         * Encodes the specified NumericErrorBarSeries message. Does not implicitly {@link epoch_proto.NumericErrorBarSeries.verify|verify} messages.
         * @param message NumericErrorBarSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.INumericErrorBarSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified NumericErrorBarSeries message, length delimited. Does not implicitly {@link epoch_proto.NumericErrorBarSeries.verify|verify} messages.
         * @param message NumericErrorBarSeries message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.INumericErrorBarSeries, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a NumericErrorBarSeries message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns NumericErrorBarSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.NumericErrorBarSeries;

        /**
         * Decodes a NumericErrorBarSeries message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns NumericErrorBarSeries
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.NumericErrorBarSeries;

        /**
         * Verifies a NumericErrorBarSeries message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a NumericErrorBarSeries message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns NumericErrorBarSeries
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.NumericErrorBarSeries;

        /**
         * Creates a plain object from a NumericErrorBarSeries message. Also converts values to other types if specified.
         * @param message NumericErrorBarSeries
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.NumericErrorBarSeries, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this NumericErrorBarSeries to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for NumericErrorBarSeries
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of an ErrorBarDef. */
    interface IErrorBarDef {

        /** ErrorBarDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** ErrorBarDef series */
        series?: (epoch_proto.IErrorBarSeries[]|null);

        /** ErrorBarDef baseLine */
        baseLine?: (epoch_proto.ILine|null);
    }

    /** Represents an ErrorBarDef. */
    class ErrorBarDef implements IErrorBarDef {

        /**
         * Constructs a new ErrorBarDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IErrorBarDef);

        /** ErrorBarDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** ErrorBarDef series. */
        public series: epoch_proto.IErrorBarSeries[];

        /** ErrorBarDef baseLine. */
        public baseLine?: (epoch_proto.ILine|null);

        /**
         * Creates a new ErrorBarDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ErrorBarDef instance
         */
        public static create(properties?: epoch_proto.IErrorBarDef): epoch_proto.ErrorBarDef;

        /**
         * Encodes the specified ErrorBarDef message. Does not implicitly {@link epoch_proto.ErrorBarDef.verify|verify} messages.
         * @param message ErrorBarDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IErrorBarDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ErrorBarDef message, length delimited. Does not implicitly {@link epoch_proto.ErrorBarDef.verify|verify} messages.
         * @param message ErrorBarDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IErrorBarDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes an ErrorBarDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ErrorBarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.ErrorBarDef;

        /**
         * Decodes an ErrorBarDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ErrorBarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.ErrorBarDef;

        /**
         * Verifies an ErrorBarDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates an ErrorBarDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ErrorBarDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.ErrorBarDef;

        /**
         * Creates a plain object from an ErrorBarDef message. Also converts values to other types if specified.
         * @param message ErrorBarDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.ErrorBarDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ErrorBarDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for ErrorBarDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a NumericErrorBarDef. */
    interface INumericErrorBarDef {

        /** NumericErrorBarDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** NumericErrorBarDef series */
        series?: (epoch_proto.INumericErrorBarSeries[]|null);

        /** NumericErrorBarDef baseLine */
        baseLine?: (epoch_proto.INumericLine|null);
    }

    /** Represents a NumericErrorBarDef. */
    class NumericErrorBarDef implements INumericErrorBarDef {

        /**
         * Constructs a new NumericErrorBarDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.INumericErrorBarDef);

        /** NumericErrorBarDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** NumericErrorBarDef series. */
        public series: epoch_proto.INumericErrorBarSeries[];

        /** NumericErrorBarDef baseLine. */
        public baseLine?: (epoch_proto.INumericLine|null);

        /**
         * Creates a new NumericErrorBarDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns NumericErrorBarDef instance
         */
        public static create(properties?: epoch_proto.INumericErrorBarDef): epoch_proto.NumericErrorBarDef;

        /**
         * Encodes the specified NumericErrorBarDef message. Does not implicitly {@link epoch_proto.NumericErrorBarDef.verify|verify} messages.
         * @param message NumericErrorBarDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.INumericErrorBarDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified NumericErrorBarDef message, length delimited. Does not implicitly {@link epoch_proto.NumericErrorBarDef.verify|verify} messages.
         * @param message NumericErrorBarDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.INumericErrorBarDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a NumericErrorBarDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns NumericErrorBarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.NumericErrorBarDef;

        /**
         * Decodes a NumericErrorBarDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns NumericErrorBarDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.NumericErrorBarDef;

        /**
         * Verifies a NumericErrorBarDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a NumericErrorBarDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns NumericErrorBarDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.NumericErrorBarDef;

        /**
         * Creates a plain object from a NumericErrorBarDef message. Also converts values to other types if specified.
         * @param message NumericErrorBarDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.NumericErrorBarDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this NumericErrorBarDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for NumericErrorBarDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a BellCurveDef. */
    interface IBellCurveDef {

        /** BellCurveDef chartDef */
        chartDef?: (epoch_proto.IChartDef|null);

        /** BellCurveDef baseData */
        baseData?: (number[]|null);

        /** BellCurveDef intervals */
        intervals?: (number|null);

        /** BellCurveDef pointsInInterval */
        pointsInInterval?: (number|null);

        /** BellCurveDef fillColor */
        fillColor?: (string|null);

        /** BellCurveDef fillOpacity */
        fillOpacity?: (number|null);
    }

    /** Represents a BellCurveDef. */
    class BellCurveDef implements IBellCurveDef {

        /**
         * Constructs a new BellCurveDef.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IBellCurveDef);

        /** BellCurveDef chartDef. */
        public chartDef?: (epoch_proto.IChartDef|null);

        /** BellCurveDef baseData. */
        public baseData: number[];

        /** BellCurveDef intervals. */
        public intervals?: (number|null);

        /** BellCurveDef pointsInInterval. */
        public pointsInInterval?: (number|null);

        /** BellCurveDef fillColor. */
        public fillColor?: (string|null);

        /** BellCurveDef fillOpacity. */
        public fillOpacity?: (number|null);

        /**
         * Creates a new BellCurveDef instance using the specified properties.
         * @param [properties] Properties to set
         * @returns BellCurveDef instance
         */
        public static create(properties?: epoch_proto.IBellCurveDef): epoch_proto.BellCurveDef;

        /**
         * Encodes the specified BellCurveDef message. Does not implicitly {@link epoch_proto.BellCurveDef.verify|verify} messages.
         * @param message BellCurveDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IBellCurveDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified BellCurveDef message, length delimited. Does not implicitly {@link epoch_proto.BellCurveDef.verify|verify} messages.
         * @param message BellCurveDef message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IBellCurveDef, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a BellCurveDef message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns BellCurveDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.BellCurveDef;

        /**
         * Decodes a BellCurveDef message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns BellCurveDef
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.BellCurveDef;

        /**
         * Verifies a BellCurveDef message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a BellCurveDef message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns BellCurveDef
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.BellCurveDef;

        /**
         * Creates a plain object from a BellCurveDef message. Also converts values to other types if specified.
         * @param message BellCurveDef
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.BellCurveDef, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this BellCurveDef to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for BellCurveDef
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a Chart. */
    interface IChart {

        /** Chart linesDef */
        linesDef?: (epoch_proto.ILinesDef|null);

        /** Chart heatMapDef */
        heatMapDef?: (epoch_proto.IHeatMapDef|null);

        /** Chart barDef */
        barDef?: (epoch_proto.IBarDef|null);

        /** Chart histogramDef */
        histogramDef?: (epoch_proto.IHistogramDef|null);

        /** Chart boxPlotDef */
        boxPlotDef?: (epoch_proto.IBoxPlotDef|null);

        /** Chart xRangeDef */
        xRangeDef?: (epoch_proto.IXRangeDef|null);

        /** Chart pieDef */
        pieDef?: (epoch_proto.IPieDef|null);

        /** Chart areaDef */
        areaDef?: (epoch_proto.IAreaDef|null);

        /** Chart numericLinesDef */
        numericLinesDef?: (epoch_proto.INumericLinesDef|null);

        /** Chart scatterDef */
        scatterDef?: (epoch_proto.IScatterDef|null);

        /** Chart waterfallDef */
        waterfallDef?: (epoch_proto.IWaterfallDef|null);

        /** Chart splineDef */
        splineDef?: (epoch_proto.ISplineDef|null);

        /** Chart numericSplineDef */
        numericSplineDef?: (epoch_proto.INumericSplineDef|null);

        /** Chart bubbleDef */
        bubbleDef?: (epoch_proto.IBubbleDef|null);

        /** Chart treemapDef */
        treemapDef?: (epoch_proto.ITreemapDef|null);

        /** Chart sankeyDef */
        sankeyDef?: (epoch_proto.ISankeyDef|null);

        /** Chart areaRangeDef */
        areaRangeDef?: (epoch_proto.IAreaRangeDef|null);

        /** Chart gaugeDef */
        gaugeDef?: (epoch_proto.IGaugeDef|null);

        /** Chart bulletDef */
        bulletDef?: (epoch_proto.IBulletDef|null);

        /** Chart timelineDef */
        timelineDef?: (epoch_proto.ITimelineDef|null);

        /** Chart errorBarDef */
        errorBarDef?: (epoch_proto.IErrorBarDef|null);

        /** Chart bellCurveDef */
        bellCurveDef?: (epoch_proto.IBellCurveDef|null);

        /** Chart numericErrorBarDef */
        numericErrorBarDef?: (epoch_proto.INumericErrorBarDef|null);
    }

    /** Represents a Chart. */
    class Chart implements IChart {

        /**
         * Constructs a new Chart.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IChart);

        /** Chart linesDef. */
        public linesDef?: (epoch_proto.ILinesDef|null);

        /** Chart heatMapDef. */
        public heatMapDef?: (epoch_proto.IHeatMapDef|null);

        /** Chart barDef. */
        public barDef?: (epoch_proto.IBarDef|null);

        /** Chart histogramDef. */
        public histogramDef?: (epoch_proto.IHistogramDef|null);

        /** Chart boxPlotDef. */
        public boxPlotDef?: (epoch_proto.IBoxPlotDef|null);

        /** Chart xRangeDef. */
        public xRangeDef?: (epoch_proto.IXRangeDef|null);

        /** Chart pieDef. */
        public pieDef?: (epoch_proto.IPieDef|null);

        /** Chart areaDef. */
        public areaDef?: (epoch_proto.IAreaDef|null);

        /** Chart numericLinesDef. */
        public numericLinesDef?: (epoch_proto.INumericLinesDef|null);

        /** Chart scatterDef. */
        public scatterDef?: (epoch_proto.IScatterDef|null);

        /** Chart waterfallDef. */
        public waterfallDef?: (epoch_proto.IWaterfallDef|null);

        /** Chart splineDef. */
        public splineDef?: (epoch_proto.ISplineDef|null);

        /** Chart numericSplineDef. */
        public numericSplineDef?: (epoch_proto.INumericSplineDef|null);

        /** Chart bubbleDef. */
        public bubbleDef?: (epoch_proto.IBubbleDef|null);

        /** Chart treemapDef. */
        public treemapDef?: (epoch_proto.ITreemapDef|null);

        /** Chart sankeyDef. */
        public sankeyDef?: (epoch_proto.ISankeyDef|null);

        /** Chart areaRangeDef. */
        public areaRangeDef?: (epoch_proto.IAreaRangeDef|null);

        /** Chart gaugeDef. */
        public gaugeDef?: (epoch_proto.IGaugeDef|null);

        /** Chart bulletDef. */
        public bulletDef?: (epoch_proto.IBulletDef|null);

        /** Chart timelineDef. */
        public timelineDef?: (epoch_proto.ITimelineDef|null);

        /** Chart errorBarDef. */
        public errorBarDef?: (epoch_proto.IErrorBarDef|null);

        /** Chart bellCurveDef. */
        public bellCurveDef?: (epoch_proto.IBellCurveDef|null);

        /** Chart numericErrorBarDef. */
        public numericErrorBarDef?: (epoch_proto.INumericErrorBarDef|null);

        /** Chart chartType. */
        public chartType?: ("linesDef"|"heatMapDef"|"barDef"|"histogramDef"|"boxPlotDef"|"xRangeDef"|"pieDef"|"areaDef"|"numericLinesDef"|"scatterDef"|"waterfallDef"|"splineDef"|"numericSplineDef"|"bubbleDef"|"treemapDef"|"sankeyDef"|"areaRangeDef"|"gaugeDef"|"bulletDef"|"timelineDef"|"errorBarDef"|"bellCurveDef"|"numericErrorBarDef");

        /**
         * Creates a new Chart instance using the specified properties.
         * @param [properties] Properties to set
         * @returns Chart instance
         */
        public static create(properties?: epoch_proto.IChart): epoch_proto.Chart;

        /**
         * Encodes the specified Chart message. Does not implicitly {@link epoch_proto.Chart.verify|verify} messages.
         * @param message Chart message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IChart, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified Chart message, length delimited. Does not implicitly {@link epoch_proto.Chart.verify|verify} messages.
         * @param message Chart message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IChart, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a Chart message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns Chart
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.Chart;

        /**
         * Decodes a Chart message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns Chart
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.Chart;

        /**
         * Verifies a Chart message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a Chart message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns Chart
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.Chart;

        /**
         * Creates a plain object from a Chart message. Also converts values to other types if specified.
         * @param message Chart
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.Chart, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this Chart to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for Chart
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a CardDefList. */
    interface ICardDefList {

        /** CardDefList cards */
        cards?: (epoch_proto.ICardDef[]|null);
    }

    /** Represents a CardDefList. */
    class CardDefList implements ICardDefList {

        /**
         * Constructs a new CardDefList.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ICardDefList);

        /** CardDefList cards. */
        public cards: epoch_proto.ICardDef[];

        /**
         * Creates a new CardDefList instance using the specified properties.
         * @param [properties] Properties to set
         * @returns CardDefList instance
         */
        public static create(properties?: epoch_proto.ICardDefList): epoch_proto.CardDefList;

        /**
         * Encodes the specified CardDefList message. Does not implicitly {@link epoch_proto.CardDefList.verify|verify} messages.
         * @param message CardDefList message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ICardDefList, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified CardDefList message, length delimited. Does not implicitly {@link epoch_proto.CardDefList.verify|verify} messages.
         * @param message CardDefList message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ICardDefList, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a CardDefList message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns CardDefList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.CardDefList;

        /**
         * Decodes a CardDefList message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns CardDefList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.CardDefList;

        /**
         * Verifies a CardDefList message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a CardDefList message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns CardDefList
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.CardDefList;

        /**
         * Creates a plain object from a CardDefList message. Also converts values to other types if specified.
         * @param message CardDefList
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.CardDefList, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this CardDefList to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for CardDefList
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a ChartList. */
    interface IChartList {

        /** ChartList charts */
        charts?: (epoch_proto.IChart[]|null);
    }

    /** Represents a ChartList. */
    class ChartList implements IChartList {

        /**
         * Constructs a new ChartList.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IChartList);

        /** ChartList charts. */
        public charts: epoch_proto.IChart[];

        /**
         * Creates a new ChartList instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ChartList instance
         */
        public static create(properties?: epoch_proto.IChartList): epoch_proto.ChartList;

        /**
         * Encodes the specified ChartList message. Does not implicitly {@link epoch_proto.ChartList.verify|verify} messages.
         * @param message ChartList message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IChartList, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ChartList message, length delimited. Does not implicitly {@link epoch_proto.ChartList.verify|verify} messages.
         * @param message ChartList message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IChartList, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a ChartList message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ChartList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.ChartList;

        /**
         * Decodes a ChartList message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ChartList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.ChartList;

        /**
         * Verifies a ChartList message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a ChartList message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ChartList
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.ChartList;

        /**
         * Creates a plain object from a ChartList message. Also converts values to other types if specified.
         * @param message ChartList
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.ChartList, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ChartList to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for ChartList
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a TableList. */
    interface ITableList {

        /** TableList tables */
        tables?: (epoch_proto.ITable[]|null);
    }

    /** Represents a TableList. */
    class TableList implements ITableList {

        /**
         * Constructs a new TableList.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ITableList);

        /** TableList tables. */
        public tables: epoch_proto.ITable[];

        /**
         * Creates a new TableList instance using the specified properties.
         * @param [properties] Properties to set
         * @returns TableList instance
         */
        public static create(properties?: epoch_proto.ITableList): epoch_proto.TableList;

        /**
         * Encodes the specified TableList message. Does not implicitly {@link epoch_proto.TableList.verify|verify} messages.
         * @param message TableList message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ITableList, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified TableList message, length delimited. Does not implicitly {@link epoch_proto.TableList.verify|verify} messages.
         * @param message TableList message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ITableList, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a TableList message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns TableList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.TableList;

        /**
         * Decodes a TableList message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns TableList
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.TableList;

        /**
         * Verifies a TableList message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a TableList message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns TableList
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.TableList;

        /**
         * Creates a plain object from a TableList message. Also converts values to other types if specified.
         * @param message TableList
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.TableList, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this TableList to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for TableList
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a TearSheet. */
    interface ITearSheet {

        /** TearSheet cards */
        cards?: (epoch_proto.ICardDefList|null);

        /** TearSheet charts */
        charts?: (epoch_proto.IChartList|null);

        /** TearSheet tables */
        tables?: (epoch_proto.ITableList|null);
    }

    /** Represents a TearSheet. */
    class TearSheet implements ITearSheet {

        /**
         * Constructs a new TearSheet.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.ITearSheet);

        /** TearSheet cards. */
        public cards?: (epoch_proto.ICardDefList|null);

        /** TearSheet charts. */
        public charts?: (epoch_proto.IChartList|null);

        /** TearSheet tables. */
        public tables?: (epoch_proto.ITableList|null);

        /**
         * Creates a new TearSheet instance using the specified properties.
         * @param [properties] Properties to set
         * @returns TearSheet instance
         */
        public static create(properties?: epoch_proto.ITearSheet): epoch_proto.TearSheet;

        /**
         * Encodes the specified TearSheet message. Does not implicitly {@link epoch_proto.TearSheet.verify|verify} messages.
         * @param message TearSheet message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.ITearSheet, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified TearSheet message, length delimited. Does not implicitly {@link epoch_proto.TearSheet.verify|verify} messages.
         * @param message TearSheet message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.ITearSheet, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a TearSheet message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns TearSheet
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.TearSheet;

        /**
         * Decodes a TearSheet message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns TearSheet
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.TearSheet;

        /**
         * Verifies a TearSheet message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a TearSheet message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns TearSheet
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.TearSheet;

        /**
         * Creates a plain object from a TearSheet message. Also converts values to other types if specified.
         * @param message TearSheet
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.TearSheet, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this TearSheet to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for TearSheet
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }

    /** Properties of a FullTearSheet. */
    interface IFullTearSheet {

        /** FullTearSheet categories */
        categories?: ({ [k: string]: epoch_proto.ITearSheet }|null);
    }

    /** Represents a FullTearSheet. */
    class FullTearSheet implements IFullTearSheet {

        /**
         * Constructs a new FullTearSheet.
         * @param [properties] Properties to set
         */
        constructor(properties?: epoch_proto.IFullTearSheet);

        /** FullTearSheet categories. */
        public categories: { [k: string]: epoch_proto.ITearSheet };

        /**
         * Creates a new FullTearSheet instance using the specified properties.
         * @param [properties] Properties to set
         * @returns FullTearSheet instance
         */
        public static create(properties?: epoch_proto.IFullTearSheet): epoch_proto.FullTearSheet;

        /**
         * Encodes the specified FullTearSheet message. Does not implicitly {@link epoch_proto.FullTearSheet.verify|verify} messages.
         * @param message FullTearSheet message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: epoch_proto.IFullTearSheet, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified FullTearSheet message, length delimited. Does not implicitly {@link epoch_proto.FullTearSheet.verify|verify} messages.
         * @param message FullTearSheet message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: epoch_proto.IFullTearSheet, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a FullTearSheet message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns FullTearSheet
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): epoch_proto.FullTearSheet;

        /**
         * Decodes a FullTearSheet message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns FullTearSheet
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): epoch_proto.FullTearSheet;

        /**
         * Verifies a FullTearSheet message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a FullTearSheet message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns FullTearSheet
         */
        public static fromObject(object: { [k: string]: any }): epoch_proto.FullTearSheet;

        /**
         * Creates a plain object from a FullTearSheet message. Also converts values to other types if specified.
         * @param message FullTearSheet
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: epoch_proto.FullTearSheet, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this FullTearSheet to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };

        /**
         * Gets the default type url for FullTearSheet
         * @param [typeUrlPrefix] your custom typeUrlPrefix(default "type.googleapis.com")
         * @returns The default type url
         */
        public static getTypeUrl(typeUrlPrefix?: string): string;
    }
}
