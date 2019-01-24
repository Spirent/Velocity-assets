<#ftl output_format="HTML">
<#assign

VISIBILITY_OF_REPORT_SECTIONS = {
"information": true,
"statistics": true,
"parameters": true,
"requirements": true,
"executionMessages": {
"ERROR": true,
"WARNING": true,
"PASS": true,
"INFORMATION": true
},
"steps": true
}

HIGHLIGHT_MAP={
"steps": [],
"issues": []
}

ENABLE_SCROLLING_IN_STEP_RESPONSE=true

RESPONSE_INFO_COLOR="#5699cd"
RESPONSE_PASS_COLOR="#4caf51"
RESPONSE_ERROR_COLOR="#ff5252"
RESPONSE_WARNING_COLOR="#ffa726"
HIGHLIGHT_TEXT_COLOR="#ffffff"

<#--Execution report information labels-->
TEST_ASSET="Automation Asset"
TEST_ASSET_LOCATION="Location"
RUNLIST_PATH="Runlist Path"
OWNER="Owner"
REPORT_DETAIL_LEVEL="Report Detail Level"
EXECUTION_STARTED="Execution Started"
EXECUTION_ENDED="Execution Ended"
EXECUTION_DURATION="Execution Duration"
REPORT_ID="Report ID"
AGENT_HOST="Agent Host"
AGENT_NAME="Agent Name"
PARAMETER_FILE_PATH="Parameter File Path"
TOPOLOGY_NAME="Topology Name"
TOPOLOGY="Topology:"
EXECUTION_STATUS="Execution Status"

<#--Execution report statistics labels-->
STATISTICS_HEADER="Statistics"
TOTAL_REPORT_ITEMS="Total report items"
TOTAL_ISSUES_COUNT="Total issues count"
PASS_COUNT="- Pass/OK"
FAIL_COUNT="- Fail"
ERROR_COUNT="- Error"
WARNING_COUNT="- Warning"
INFORMATION_COUNT="- Information"

AGENT_REQUIREMENTS_HEADER="Agent Requirements"

CHARTS_HEADER="Charts"

<#--Parameters section labels-->
PARAMETERS_HEADER="Parameters"
PARAMETER_COLUMN_NAMES=["#", "Name", "Value"]

<#-- Extracted Data section label -->
EXTRACTEDDATA_HEADER="Extracted Data"
EXTRACTEDDATA_COLUMN_NAMES=["Extracted Data Tag", "Value(s)"]

<#--Execution messages labels-->
EXECUTION_MESSAGES_HEADER="Execution Messages"
EXECUTION_MESSAGE_COLUMN_NAMES=["Step #", "Originator", "Message"]

<#--Steps section labels-->
STEP_HEADER="Steps"
STEP_COLUMN_NAMES=["Step #", "Action", "Start Time", "Duration"]
STEP_ACTION="Action:"
STEP_COMMAND="Command:"
RESPONSE_HEADER="RESPONSE"
POST_PROCESSING_HEADER="POST PROCESSING"
POST_PROCESSING_COLUMN_NAMES=["#", "Action", "Description"]
>

<!DOCTYPE HTML>
<html>
<@compress>
<head>
	<title></title>
	<style type="text/css">
			<#macro addSelectCssStyles>
			-webkit-touch-callout: auto;
			-webkit-user-select: auto;
			-khtml-user-select: auto;
			-moz-user-select: auto;
			-ms-user-select: auto;
			user-select: auto;
			</#macro>

			<#macro generateIconFontStyle content color fontSize>
			content: "\${content}";
			font-style: normal;
			font-weight: normal;
			font-variant: normal;
			text-transform: none;
			color: ${color};
			font-size: ${fontSize};
			</#macro>

			<#macro addAlignItemsCss alignment>
			-webkit-box-align: ${alignment};
			-ms-flex-align: ${alignment};
			-webkit-align-items: ${alignment};
			-moz-align-items: ${alignment};
			align-items: ${alignment};
			</#macro>

			<#macro includeJustifyContent alignment>
			-webkit-justify-content: ${alignment};
			-moz-justify-content: ${alignment};
			justify-content: ${alignment};
			</#macro>

			<#macro displayFlexCss>
			display: -webkit-box;
			display: -webkit-flex;
			display: -moz-flex;
			display: -ms-flexbox;
			display: flex;
			</#macro>

			<#macro includeFlexShrink shrink>
			-webkit-flex-shrink: ${shrink};
			-moz-flex-shrink: ${shrink};
			-ms-flex-negative: ${shrink};
			flex-shrink: ${shrink};
			</#macro>

			<#macro includeBorderRadius radius>
			-webkit-border-radius: ${radius};
			-moz-border-radius: ${radius};
			-ms-border-radius: ${radius};
			-o-border-radius: ${radius};
			border-radius: ${radius};
			</#macro>

		@page {
			size: A4;
			margin: 10px;
		}

		body, div, dl, dt, dd, ul, ol, li, h1, h2, h3, h4, h5, h6, pre, form, fieldset, input, button, textarea, p, blockquote, th, td {
			margin: 0;
			padding: 0; }

		table {
			border-collapse: collapse;
			border-spacing: 0;
			page-break-inside:auto
		}

		tr {
			page-break-inside:avoid;
			page-break-after:auto
		}

		fieldset, img {
			border: 0; }

		address, caption, cite, code, dfn, em, strong, th, var {
			font-style: normal;
			font-weight: normal; }

		ol, ul {
			list-style: none; }

		caption, th {
			text-align: left; }

		h1, h2, h3, h4, h5, h6 {
			font-size: 100%;
			font-weight: normal; }

		q:before, q:after {
			content: ""; }

		abbr, acronym {
			border: 0; }

		*, *:before, *:after {
			-moz-box-sizing: border-box;
			-webkit-box-sizing: border-box;
			box-sizing: border-box; }

		.b-board {
			max-width: 800px;
			background-color: #ffffff;
			border: solid 1px #c4c4c4;
			margin: 10px auto;
			<@includeBorderRadius radius="4px"/>
		}

		@media print {
			.b-board{
				border: none;
				margin: 30px auto;
			}
		}

		.b-board .b-board__item {
			margin: 0 20px 10px 20px;
		}

		.b-board .b-board__header {
			margin: 10px 10px 10px 10px
		}

		.b-board-header {
			<@displayFlexCss/>
			<@includeJustifyContent alignment="center"/>
			<@addAlignItemsCss alignment="center"/>
		}

		.b-board-header .b-board-header__title {
			margin-left: 25px;
			flex-grow: 1;
		}

		.b-board-header .b-board-header__images {
			margin: 0 20px 0 20px;
		}

		.b-composite-title__item {
			margin-top: 10px;
			max-width: 430px;
			word-wrap: break-word;
		}

		.b-card {
			text-align: left;
			background: #ffffff;
			overflow: hidden;
		}

		.b-card.b-card_with-border {
			border: solid 1px #c4c4c4;
			<@includeBorderRadius radius="4px"/>
		}

		.b-card-header {
			width: 100%;
			background: #ffffff;
		}

		.b-card-header-main {
			width: 100%;
			-webkit-box-pack: justify;
			-ms-flex-pack: justify;
			<@includeJustifyContent alignment="space-between"/>
			<@displayFlexCss/>
			<@addAlignItemsCss alignment="center"/>
		}

		.b-card-header-main .b-card-header-main__title {
			overflow: hidden;
			<@includeFlexShrink shrink=1/>
		}

		.b-card-header-title {
			width: 100%;
			position: relative;
			height: 30px;
			<@displayFlexCss/>
			<@addAlignItemsCss alignment="center"/>
		}

		.b-card-header-title .b-card-header-title__name {
			overflow: hidden;
			<@includeFlexShrink shrink=1/>
		}

		.b-card-header-title-name {
			width: 100%;
			<@displayFlexCss/>
		}

		.b-card-header-title-name .b-card-header-title-name__name {
			overflow: hidden;
			margin-right: 5px;
			<@includeFlexShrink shrink=1/>
		}

		.b-text {
			display: inline-block;
			font-size: 12px;
			font-family: "Open Sans Regular";
			word-break: break-all;
			word-wrap: break-word;
			<@addSelectCssStyles/>
		}

			<#if ENABLE_SCROLLING_IN_STEP_RESPONSE>
			.b-text_response {
				word-break: normal;
				white-space: pre;
			}
			</#if>

		@media print {
			.b-text_response {
				word-break: break-word;
			}
		}

		.b-text_highlighted-information {
			background-color: ${RESPONSE_INFO_COLOR};
			color: ${HIGHLIGHT_TEXT_COLOR};
		}

		.b-text_highlighted-pass {
			background-color: ${RESPONSE_PASS_COLOR};
			color: ${HIGHLIGHT_TEXT_COLOR};
		}

		.b-text_highlighted-warning {
			background-color: ${RESPONSE_WARNING_COLOR};
		}

		.b-text_highlighted-error {
			background-color: ${RESPONSE_ERROR_COLOR};
			color: ${HIGHLIGHT_TEXT_COLOR};
		}

		.b-text_monospace {
			font-family: monospace;
		}

		.b-text_pre-wrap {
			white-space: pre-wrap;
		}

		.b-text.b-text_increased {
			font-size: 13px;
		}

		.b-text.b-text_middle-title {
			font-family: "Open Sans Semibold";
			font-size: 20px;
		}

		.b-text.b-text_title {
			font-size: 26px;
		}

		.b-text.b-text_accented {
			font-family: "Open Sans Semibold";
		}

		.b-text.b-text_description {
			color: #696969;
		}

		.b-text.b-text_dove-gray {
			color: #696969;
		}

		.b-text.b-text_multiline {
			white-space: pre-wrap;
		}

		.b-text-container {
			font-size: 0;
		}

		.b-link {
			color: #0b65ac;
			text-decoration: none;
			cursor: pointer;
			font-family: "Open Sans Regular";
			font-size: 12px;
		}

		.b-link.b-link_text-wrap {
			display: inline-block;
			word-break: break-all;
			word-wrap: break-word;
		}

		.b-link.b-link_full-size {
			position: absolute;
			top: 0;
			bottom: 0;
			left: 0;
			right: 0;
		}

		.g-col-label {
			width: auto;
		}

		.g-col-field {
			width: 100%;
		}

		.g-col-index {
			width: 75px;
		}
		
		.g-col-short-name {
			width: 90px
		}
		
		.g-col-step {
			width: 40px;
		}
		
		.g-col-start-time {
			width: 60px
		}
		
		.g-col-step-action {
			width: 100%;
		}

		.g-col-step-start-time {
			width: 115px;
		}

		.g-col-step-duration {
			width: 115px;
		}

		.g-col-originator {
			width: 135px;
		}

		.g-col-message {
			width: 100%;
		}

		.g-col-action {
			width: 100px;
		}

		.b-table-form {
			width: 100%;
			<@addSelectCssStyles/>
		}

		.b-table-form-row .b-table-form__cell {
			vertical-align: top;
		}

		.b-table-form-row .b-table-form__cell.b-table-form__cell_label {
			padding: 4px 0 0 10px;
			text-align: left;
			font-weight: normal;
		}

		.b-table-form-row .b-table-form__cell.b-table-form__cell_field {
			padding: 4px 0 0 30px;
		}

		.b-table-form-cell {
			position: relative;
		}

		.b-table-form-cell .b-table-form-cell__text {
			position: relative;
			line-height: 17px;
		}

		.b-table-form-cell .b-table-form-cell__label {
			overflow: hidden;
		}

		.b-label {
			font-size: 12px;
			font-family: "Open Sans Semibold";
			color: #262626;
			<@addSelectCssStyles/>
		}

		.b-label.b-label_form {
			overflow: hidden;
			white-space: nowrap;
		}

		.b-test-case-result-big-circle-icon {
			-webkit-box-direction: normal;
			-webkit-box-orient: vertical;
			-webkit-flex-direction: column;
			-moz-flex-direction: column;
			-ms-flex-direction: column;
			flex-direction: column;
			width: 160px;
			height: 160px;
			<@includeBorderRadius radius="100%"/>
			<@displayFlexCss/>
			<@addAlignItemsCss alignment="center"/>
		}

		.b-test-case-result-big-circle-icon.b-test-case-result-big-circle-icon_pass {
			background-color: #4caf51;
		}

		.b-test-case-result-big-circle-icon.b-test-case-result-big-circle-icon_indeterminate {
			background-color: #ffa726;
		}

		.b-test-case-result-big-circle-icon.b-test-case-result-big-circle-icon_abort, .b-test-case-result-big-circle-icon.b-test-case-result-big-circle-icon_cancel, .b-test-case-result-big-circle-icon.b-test-case-result-big-circle-icon_error, .b-test-case-result-big-circle-icon.b-test-case-result-big-circle-icon_fail {
			background-color: #ff5252;
		}

		.b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__icon {
			margin-top: 26px;
		}

		.b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__icon.b-test-case-result-big-circle-icon__icon_cancel, .b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__icon.b-test-case-result-big-circle-icon__icon_abort {
			margin-right: 6px;
		}

		.b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__icon.b-test-case-result-big-circle-icon__icon_error, .b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__icon.b-test-case-result-big-circle-icon__icon_fail {
			margin-right: 2px;
		}

		.b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__label {
			margin-top: -10px;
		}

		.b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__label.b-test-case-result-big-circle-icon__label_indeterminate {
			margin-top: -25px;
		}

		.b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__label.b-test-case-result-big-circle-icon__label_pass, .b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__label.b-test-case-result-big-circle-icon__label_abort, .b-test-case-result-big-circle-icon .b-test-case-result-big-circle-icon__label.b-test-case-result-big-circle-icon__label_cancel {
			margin-top: -15px;
		}

		.b-icon {
			font-family: "Velocity Icons";
			cursor: default;
			outline: none;
			<@addSelectCssStyles/>
		}

		.b-icon:before {
			display: block;
		}

		.b-icon.b-icon_status-canceled:before {
			<@generateIconFontStyle content="E611" fontSize="24px" color="#ff5252"/>
		}

		.b-icon.b-icon_status-canceled.b-icon_status-canceled_big:before {
			<@generateIconFontStyle content="E636" fontSize="80px" color="#ffffff"/>
		}

		.b-icon.b-icon_status-skipped:before {
			<@generateIconFontStyle content="E611" fontSize="24px" color="#696969"/>
		}

		.b-icon.b-icon_status-completed:before {
			<@generateIconFontStyle content="E60C" fontSize="24px" color="#4caf51"/>
		}

		.b-icon.b-icon_status-completed.b-icon_status-completed_big:before {
			<@generateIconFontStyle content="E61D" fontSize="80px" color="#ffffff"/>
		}

		.b-icon.b-icon_status-completed-warn:before {
			<@generateIconFontStyle content="E60C" fontSize="24px" color="#ffa726"/>
		}

		.b-icon.b-icon_status-accepted:before {
			<@generateIconFontStyle content="E60D" fontSize="24px" color="#4caf51"/>
		}

		.b-icon.b-icon_status-pending-warn:before {
			<@generateIconFontStyle content="E60E" fontSize="24px" color="#ffa726"/>
		}

		.b-icon.b-icon_status-pending:before {
			<@generateIconFontStyle content="E60E" fontSize="24px" color="#0b65ac"/>
		}

		.b-icon.b-icon_status-failed:before {
			<@generateIconFontStyle content="E60F" fontSize="24px" color="#ff5252"/>
		}

		.b-icon.b-icon_status-failed.b-icon_status-failed_big:before {
			<@generateIconFontStyle content="E600" fontSize="80px" color="#ffffff"/>
		}

		.b-icon.b-icon_status-info:before {
			<@generateIconFontStyle content="E643" fontSize="24px" color="#5699cd"/>
		}

		.b-icon.b-icon_status-warning:before {
			<@generateIconFontStyle content="E60F" fontSize="24px" color="#ffa726"/>
		}

		.b-icon.b-icon_status-declined:before {
			<@generateIconFontStyle content="E610" fontSize="24px" color="#ff5252"/>
		}

		.b-icon.b-icon_status-terminated:before {
			<@generateIconFontStyle content="E611" fontSize="24px" color="#ff5252"/>
		}

		.b-icon.b-icon_status-aborted:before {
			<@generateIconFontStyle content="E609" fontSize="24px" color="#ff5252"/>
		}

		.b-icon.b-icon_status-aborted.b-icon_status-aborted_big:before {
			<@generateIconFontStyle content="E636" fontSize="80px" color="#ffffff"/>
		}

		.b-icon.b-icon_status-indeterminate:before {
			<@generateIconFontStyle content="E645" fontSize="24px" color="#ffa726"/>
		}

		.b-icon.b-icon_status-indeterminate.b-icon_status-indeterminate_big:before {
			<@generateIconFontStyle content="E62A" fontSize="80px" color="#ffffff"/>
		}

		.b-test-case-result-label {
			color: #ffffff;
			font-size: 15px;
			font-family: "Open Sans Semibold";
			text-transform: uppercase;
		}

		table {
			border-collapse: collapse;
			border-spacing: 0;
		}

		.b-table {
			width: 100%;
			table-layout: fixed;
		}

		.b-table-row {
			background: #fafafa;
		}

		.b-table-row.b-table-row_colored:nth-child(even) {
			background: #f3f3f3;
		}

		.b-table-row.b-table-row_header {
			background: #ffffff;
		}

		.b-table-row.b-table-row_big {
			height: 36px;
		}

		.b-table__cell {
			min-height: 20px;
			vertical-align: top;
			border-top: 1px solid #dbdbdb;
			padding: 0 5px 0 0;
		}

		.b-table__cell.b-table__cell_no-border {
			border: none;
		}

		.b-table__cell:first-child {
			padding-left: 20px;
		}

		.b-table__cell.b-table__cell_header {
			border-top: none;
			position: relative;
		}

		.b-table-cell.b-table-cell_header {
			text-transform: capitalize;
			overflow: hidden;
			white-space: nowrap;
			margin-top: 1px;
		}
		.b-table-cell .b-table-cell__title.b-table-cell__title_header, .b-table-cell .b-table-cell__title.b-table-cell__title_badge, .b-table-cell .b-table-cell__title.b-table-cell__title_lock {
			max-width: 100%;
			float: left;
		}

		.b-flex-row {
			<@displayFlexCss/>
			<@addAlignItemsCss alignment="flex-start"/>
		}

		.b-flex-row.b-flex-row_response {
			min-height: 18px;
		}

		.b-flex-row__item {
			margin-right: 5px;
		}

		.b-flex-row__originator {
			margin-left: 16px;
			width: 100px;
			word-wrap: break-word;
		}

		.b-flex-row-item__icon {
			margin: -4px 0 0 -4px;
			position: absolute;
		}

		.b-step-details__content {
			margin-bottom: 10px;
			margin-top: 10px;
			margin-right: 30px;
		}

		.b-response {
			background: #f3f3f3;
			position: relative;
			width: 100%;
			min-height: 50px;
			border: solid 1px #c4c4c4;
			overflow-x: auto;
			<@includeBorderRadius radius="4px"/>
		}

		.b-response__content {
			display: inline-block;
			margin: 10px;
		}

		.b-topology-preview {
			position: relative;
		}

		.b-topology-preview__preview {
			margin-top: 10px;
		}

		.b-topology-preview-iframe {
			display: block;
			width: 100%;
			height: 270px;
			border: solid 1px #c4c4c4;
			<@includeBorderRadius radius="4px"/>
		}
		.b-topology-preview-image {
			display: block;
			max-width: 100%;
		}
		@media all and (-ms-high-contrast: none), (-ms-high-contrast: active) {
			.b-topology-preview-image
			{
				display: block;
				max-width: 40%;
			}
		}
		.b-table-form-field.b-table-form-field_status {
			margin-left: 25px;
			margin-top: 13px;
		}
		.b-test-case-chart {
			max-width: 100%;
		}
		.b-logo-image {
			max-width: 200px;
			max-height: 100px;
		}
		.b-board-header-images {
			flex-direction: column;
		}
		.b-board-header-images__item {
			display: flex;
			margin-bottom: 5px;
			<@includeJustifyContent alignment="center"/>
		}
			<#include "embedded_fonts.ftl">
	</style>
</head>
</@compress>

<#function getDetailLevelMessage>
	<#switch model.report.detailLevel>
		<#case "REPORT_ONLY">
			<#return "Nothing but the report-level details, including status and result"/>
			<#break>
		<#case "ERROR_ISSUES_ONLY">
			<#return "Include only error execution messages"/>
			<#break>
		<#case "ERROR_ISSUES_WITH_STEPS">
			<#return "Include only error execution messages and associated steps"/>
			<#break>
		<#case "ALL_ISSUES_ERROR_STEPS">
			<#return "Include all execution messages (and steps that have an error)"/>
			<#break>
		<#case "ALL_ISSUES_ALL_STEPS">
			<#return "Include all execution messages and steps"/>
			<#break>
	</#switch>
</#function>

<#macro renderResultIcon>
	<#switch model.report.result>
		<#case "ABORT">
			<@renderCircleIcon classPrefix="abort" label="Aborted" status="aborted"/>
			<#break>
		<#case "CANCEL">
			<@renderCircleIcon classPrefix="cancel" label="Canceled" status="canceled"/>
			<#break>
		<#case "ERROR">
			<@renderCircleIcon classPrefix="error" label="Error" status="failed"/>
			<#break>
		<#case "FAIL">
			<@renderCircleIcon classPrefix="fail" label="Failed" status="failed"/>
			<#break>
		<#case "INDETERMINATE">
			<@renderCircleIcon classPrefix="indeterminate" label="Indeterminate" status="indeterminate"/>
			<#break>
		<#case "PASS">
			<@renderCircleIcon classPrefix="pass" label="Passed" status="completed"/>
			<#break>
	</#switch>
</#macro>

<#function getStatusMessage>
	<#if model.report.failureReason?has_content>
		<#return model.report.failureReason/>
	</#if>
	<#switch model.report.status>
		<#case "START_FAILED">
			<#return "Start failed"/>
			<#break>
		<#case "ABORTED">
			<#return "Aborted"/>
			<#break>
		<#case "AGENT_NOT_RESPONDING">
			<#return "Agent not responding"/>
			<#break>
		<#case "COMPLETED">
			<#return "Completed"/>
			<#break>
		<#case "DISPATCHING">
			<#return "Dispatching"/>
			<#break>
		<#case "IN_PROGRESS">
			<#return "In progress"/>
			<#break>
		<#case "NOT_BEGUN">
			<#return "Not begun"/>
			<#break>
	</#switch>
</#function>

<#macro renderMessageSeverityIcon status>
	<#switch status>
		<#case "WARNING">
		<div class="b-icon b-icon_status-warning"></div>
			<#break>
		<#case "PASS">
		<div class="b-icon b-icon_status-completed"></div>
			<#break>
		<#case "INFORMATION">
		<div class="b-icon b-icon_status-info"></div>
			<#break>
		<#case "ERROR">
		<div class="b-icon b-icon_status-failed"></div>
			<#break>
	</#switch>
</#macro>

<#macro renderMessageSeverityIconByCode status>
	<#switch status>
		<#case "1">
		<div class="b-icon b-icon_status-completed"></div>
			<#break>
		<#case "2">
		<div class="b-icon b-icon_status-info"></div>
			<#break>
		<#case "3">
		<div class="b-icon b-icon_status-warning"></div>
			<#break>
		<#case "4">
		<div class="b-icon b-icon_status-failed"></div>
			<#break>
	</#switch>
</#macro>

<#macro renderCircleIcon classPrefix label status>
<div class="b-test-case-result-big-circle-icon b-test-case-result-big-circle-icon_${classPrefix}">
	<div class="b-test-case-result-big-circle-icon__icon b-test-case-result-big-circle-icon__icon_${classPrefix}">
		<div class="b-status-icon">
			<div class="b-status-icon__icon">
				<div class="b-icon b-icon_status-${status} b-icon_status-${status}_big"></div>
			</div>
		</div>
	</div>
	<div class="b-test-case-result-big-circle-icon__label b-test-case-result-big-circle-icon__label_${classPrefix}">
		<div class="b-test-case-result-label">${label}</div>
	</div>
</div>
</#macro>

<#macro card headerTitle>
<div class="b-board__item">
	<div class="b-card">
		<#if headerTitle?has_content>
			<div class="b-card-header">
				<div class="b-card-header__main">
					<div class="b-card-header-main">
						<div class="b-card-header-main__title">
							<div class="b-card-header-title">
								<div class="b-card-header-title__name">
									<div class="b-card-header-title-name">
										<div class="b-card-header-title-name__name">
											<div class="b-text b-text_middle-title">${headerTitle}</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</#if>
		<div class="b-card__form">
			<table id="reportHeader" class="b-table-form">
				<colgroup>
					<col class="g-col-label">
					<col class="g-col-field">
				</colgroup>
				<tbody class="b-table-form__body">
					<#nested>
				</tbody>
			</table>
		</div>
	</div>
</div>
</#macro>

<#macro renderFormRow label="" field="">
	<#if !(field?has_content)>
		<#return/>
	</#if>
<tr class="b-table-form-row">
	<th class="b-table-form__cell b-table-form__cell_label">
		<div class="b-table-form-cell b-table-form-cell_label">
			<div class="b-table-form-cell__label">
				<div class="b-label b-label_form">${label}:</div>
			</div>
		</div>
	</th>
	<td class="b-table-form__cell b-table-form__cell_field">
		<div class="b-table-form-field">
			<div class="b-table-form-field__cell">
				<div class="b-table-form-cell">
					<div class="b-table-form-cell__text">
						<div class="b-text b-text_word-wrap b-text_pre-wrap">${field}</div>
					</div>
				</div>
			</div>
		</div>
	</td>
</tr>
</#macro>

<#macro renderTableFrame title colNames colGroups containerClass="b-board">
<div class="${containerClass}__item">
	<div class="b-text b-text_middle-title">${title}</div>
</div>
<div class="${containerClass}__item">
	<div class="b-card b-card_with-border">
		<table class="b-table">
			<colgroup>
				<#list colGroups as colGroup>
					<col class="${colGroup}">
				</#list>
			</colgroup>
			<thead class="b-table__header">
			<tr class="b-table-row b-table-row_header">
				<#list colNames as colName>
					<th class="b-table__cell b-table__cell_header">
						<div class="b-table-cell b-table-cell_header">
							<div class="b-table-cell__title b-table-cell__title_header">
								<div class="b-text b-text_increased b-text_accented b-text_table">${colName}</div>
							</div>
						</div>
					</th>
				</#list>
			</tr>
			</thead>
		</table>
		<div class="b-card__table">
			<table id="executionMessages" class="b-table">
				<colgroup>
					<#list colGroups as colGroup>
						<col class="${colGroup}">
					</#list>
				</colgroup>
				<tbody class="b-table__body">
					<#nested>
				</tbody>
			</table>
		</div>
	</div>
</div>
</#macro>

<#macro renderParameters>
	<#if !(model.report.parameters?has_content) || !VISIBILITY_OF_REPORT_SECTIONS.parameters>
		<#return/>
	</#if>
	<@renderTableFrame title=PARAMETERS_HEADER colNames=PARAMETER_COLUMN_NAMES colGroups=["g-col-index", "g-col-name", "g-col-parameter-file-value"]>
		<#list model.report.parameters as parameter>
		<tr class="b-table-row b-table-row_colored">
			<td class="b-table__cell">
				<div class="b-table-cell">
					<div class="b-table-cell__item">
						<div class="b-text">${parameter.index}</div>
					</div>
				</div>
			</td>
			<td class="b-table__cell">
				<div class="b-table-cell">
					<div class="b-table-cell__item">
						<div class="b-text">${parameter.name}</div>
					</div>
				</div>
			</td>
			<td class="b-table__cell">
				<#if parameter.value?has_content>
					<div class="b-table-cell">
						<div class="b-table-cell__item">
							<#if parameter.masked?has_content && parameter.masked>
								<div class="b-text">****</div>
							<#else>
								<div class="b-text">${parameter.value}</div>
							</#if>
						</div>
					</div>
				</#if>
			</td>
		</tr>
		</#list>
	</@renderTableFrame>
</#macro>

<#macro renderExtractedData>
	<#if !(model.report.extractedData?has_content)>
		<#return/>
	</#if>
	<@renderTableFrame title=EXTRACTEDDATA_HEADER colNames=EXTRACTEDDATA_COLUMN_NAMES
		colGroups=["g-col-start-time", "g-col-short-name", "g-col-short-name", "g-col-step", "g-col-step", 
		"g-col-label", "g-col-label"]>
		<#list model.report.extractedData as extractedData>
		<tr class="b-table-row b-table-row_colored">
			<td class="b-table__cell">
				<div class="b-table-cell">
					<div class="b-table-cell__item">
						<div class="b-text">${extractedData.tag}</div>
					</div>
				</div>
			</td>
			<td class="b-table__cell">
				<#if extractedData.data?has_content>
					<div class="b-table-cell">
						<#list extractedData.data as item>
							<div class="b-table-cell__item">
								<div class="b-text">${item}</div>
							</div>
						</#list>
					</div>
				</#if>
			</td>
		</tr>
		</#list>
	</@renderTableFrame>
</#macro>

<#macro renderStepsTable>
	<#if !(model.steps?has_content) || !VISIBILITY_OF_REPORT_SECTIONS.steps>
		<#return/>
	</#if>
	<@renderTableFrame title=STEP_HEADER colNames=STEP_COLUMN_NAMES colGroups=["g-col-index", "g-col-step-action", "g-col-step-start-time", "g-col-step-duration"]>
		<#list model.steps as step>
			<#assign background=getStepHighlighting(step)>
			<@compress>
			<tr class="b-table-row b-table-row_big" style="${background}">
				<td class="b-table__cell" title="${step.stepId}">
					<div class="b-table-cell">
						<div class="b-table-cell__item">
							<a class="b-text" name="step_${step.stepId}" id="step_${step.stepId}">
								<span class="b-text">${step.stepId}</span>
							</a>
						</div>
					</div>
				</td>
				<td class="b-table__cell">
					<div class="b-table-cell">
						<#if step.action?has_content>
							<div class="b-table-cell__item">
								<div class="b-flex-row">
									<div class="b-flex-row__item">
										<div class="b-label">${STEP_ACTION}</div>
									</div>
									<div class="b-flex-row__item">
										<div class="b-text b-text_accented">${step.action}</div>
									</div>
								</div>
							</div>
						</#if>
						<#if step.command?has_content>
							<div class="b-table-cell__item">
								<div class="b-flex-row">
									<div class="b-flex-row__item">
										<div class="b-label">${STEP_COMMAND}</div>
									</div>
									<div class="b-flex-row__item">
										<div class="b-text b-text_description b-text_multiline">${step.command}</div>
									</div>
								</div>
							</div>
						</#if>
					</div>
				</td>
				<td class="b-table__cell">
					<div class="b-table-cell">
						<div class="b-table-cell__item">
							<div class="b-text">${step.startOffset}</div>
						</div>
					</div>
				</td>
				<td class="b-table__cell">
					<div class="b-table-cell">
						<div class="b-table-cell__item">
							<div class="b-text">${step.duration}</div>
						</div>
					</div>
				</td>
			</tr>
			</@compress>
			<#--Step Response Should be uncompressed-->
			<@renderStepResponse step=step background=background/>
			<@compress>
				<#if step.postProcessing?has_content>
				<tr class="b-table-row b-table-row_response" style="${background}">
					<td/>
					<td class="b-table__cell b-table__cell_no-border" colSpan="5">
						<div class="b-table-cell">
							<div class="b-table-cell__item">
								<div class="b-step-details">
									<div class="b-step-details__header">
										<div class="b-text b-text_dove-gray b-text_accented b-text_increased">${POST_PROCESSING_HEADER}</div>
									</div>
									<div class="b-step-details__content">
										<@renderPostProcessing actions=step.postProcessing/>
									</div>
								</div>
							</div>
						</div>
					</td>
				</tr>
				</#if>
			</@compress>
		</#list>
	</@renderTableFrame>
</#macro>

<#function getStepHighlighting step>
	<#list HIGHLIGHT_MAP.steps as highlightBlock>
		<#if step[highlightBlock.field] == highlightBlock.pattern>
			<#return "background-color: ${highlightBlock.color};">
		</#if>
	</#list>
	<#return "">
</#function>

<#macro renderStepResponse step background>
	<#if step.response?has_content>
	<tr class="b-table-row b-table-row_response" style="${background}">
		<td/>
		<td class="b-table__cell b-table__cell_no-border" colSpan="5">
			<div class="b-table-cell">
				<div class="b-table-cell__item">
					<div class="b-step-details">
						<div class="b-step-details__header">
							<div class="b-text b-text_dove-gray b-text_accented b-text_increased">${RESPONSE_HEADER}</div>
						</div>
						<div class="b-step-details__content">
							<div class="b-response">
								<div class="b-response__content">
									<#assign lines=step.response?split("(\r\n|\r|\n)|$", 'r')>
									<#assign highlighting=model.highlighting[step.stepId]!>
									<#if highlighting?has_content>
										<#list lines as responseLine>
											<#if highlighting[responseLine?index?string]?has_content>
												<@renderHighlightedLine line=responseLine highlighting=highlighting[responseLine?index?string]/>
											<#else>
												<div class="b-flex-row b-flex-row_response">
													<div class="b-flex-row__text">
														<span class="b-text b-text_monospace b-text_response">${responseLine}</span>
													</div>
												</div>
											</#if>
										</#list>
									<#else>
										<#list lines as responseLine>
											<div class="b-flex-row b-flex-row_response">
												<div class="b-flex-row__text">
													<span class="b-text b-text_monospace b-text_response">${responseLine}</span>
												</div>
											</div>
										</#list>
									</#if>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</td>
	</tr>
	</#if>
</#macro>

<#macro renderHighlightedLine line highlighting>
<div class="b-flex-row b-flex-row_response">
	<#assign prevColumn = 0>
	<#assign startColumn=highlighting[0].startColumn>
	<div class="b-text-container">
		<#list highlighting as block>
			<#assign startColumn=block.startColumn>
			<#assign endColumn=min(block.endColumn, line?length)-1>
			<#if block.endOnOtherLine>
				<#assign endColumn=line?length-1>
			</#if>
			<#if startColumn < line?length>
				<#if prevColumn <= startColumn-1>
					<span class="b-text b-text_monospace b-text_response b-text_pre-wrap">${line[prevColumn..startColumn-1]}</span>
				</#if>
				<span class="b-text b-text_monospace b-text_response b-text_pre-wrap ${severityClass(block.severity)}">${line[startColumn..endColumn]}</span>
				<#assign prevColumn = endColumn+1>
			</#if>
		</#list>
		<#assign lineLength=line?length - 1>
		<#if prevColumn <= lineLength>
			<span class="b-text b-text_monospace b-text_response b-text_pre-wrap">${line[prevColumn..lineLength]}</span>
		</#if>
	</div>
</div>
</#macro>

<#function min x y>
	<#if (x<y)><#return x><#else><#return y></#if>
</#function>

<#function severityClass severity>
	<#switch severity>
		<#case 0>
			<#return "">
			<#break>
		<#case 1>
			<#return "b-text_highlighted-information">
			<#break>
		<#case 2>
			<#return "b-text_highlighted-pass">
			<#break>
		<#case 3>
			<#return "b-text_highlighted-warning">
			<#break>
		<#case 4>
			<#return "b-text_highlighted-error">
			<#break>
	</#switch>
</#function>

<#macro renderPostProcessing actions>
<div class="b-post-processing">
	<@renderTableFrame title="" colNames=POST_PROCESSING_COLUMN_NAMES colGroups=["g-col-index", "g-col-action", "g-col-parameter-file-value"] containerClass="b-post-processing">
		<#list actions as action>
			<tr class="b-table-row b-table-row_colored">
				<td class="b-table__cell">
					<div class="b-table-cell">
						<div class="b-table-cell__item">
							<div class="b-text">${action.index}</div>
						</div>
					</div>
				</td>
				<td class="b-table__cell">
					<div class="b-table-cell">
						<div class="b-table-cell__item">
							<div class="b-text">${action.action}</div>
						</div>
					</div>
				</td>
				<td class="b-table__cell">
					<div class="b-table-cell">
						<div class="b-table-cell__item">
							<div class="b-text">${action.description}</div>
						</div>
					</div>
				</td>
			</tr>
		</#list>
	</@renderTableFrame>
</div>
</#macro>

<#macro renderExecutionIssues>
	<#if !(model.issues?has_content)>
		<#return/>
	</#if>
	<@renderTableFrame title=EXECUTION_MESSAGES_HEADER colNames=EXECUTION_MESSAGE_COLUMN_NAMES colGroups=["g-col-index", "g-col-originator", "g-col-message"]>
		<#list model.issues as issue>
			<#if VISIBILITY_OF_REPORT_SECTIONS.executionMessages[issue.severity]>
			<tr class="b-table-row b-table-row_colored" style="${getIssueHighlighting(issue)}">
				<td class="b-table__cell">
					<#if issue.stepId?has_content>
						<div class="b-table-cell">
							<div class="b-table-cell__item">
								<a class="b-link b-link_text-wrap" href="#step_${issue.stepId}">${issue.stepId}</a>
							</div>
						</div>
					</#if>
				</td>
				<td class="b-table__cell">
					<div class="b-table-cell">
						<div class="b-table-cell__item">
							<div class="b-flex-row">
								<div class="b-flex-row__item">
									<div class="b-flex-row-item">
										<div class="b-flex-row-item__icon">
											<@renderMessageSeverityIcon status=issue.severity/>
                                            <@renderMessageSeverityIconByCode status=issue.severity/>
										</div>
									</div>
								</div>
								<div class="b-flex-row__originator">
									<div class="b-text">${issue.originator}</div>
								</div>
							</div>
						</div>
					</div>
				</td>
				<td class="b-table__cell">
					<div class="b-table-cell">
						<div class="b-table-cell__item">
							<div class="b-text">${issue.message}</div>
						</div>
					</div>
				</td>
			</tr>
			</#if>
		</#list>
	</@renderTableFrame>
</#macro>

<#function getIssueHighlighting issue>
	<#list HIGHLIGHT_MAP.issues as highlightBlock>
		<#if issue[highlightBlock.field] == highlightBlock.pattern>
			<#return "background-color: ${highlightBlock.color};">
		</#if>
	</#list>
	<#return "">
</#function>

<#macro renderReportHeader>
<div class="b-board__header">
	<div class="b-board-header">
		<div class="b-board-header__status-icon">
			<@renderResultIcon/>
		</div>
		<div class="b-board-header__title">
			<div class="b-composite-title">
				<#if model.headlineText?has_content>
					<div class="b-composite-title__item">
						<div class="b-text b-text_title">${model.headlineText}</div>
					</div>
				</#if>
				<div class="b-composite-title__item">
					<div class="b-text b-text_middle-title">${model.report.testName}</div>
				</div>
			</div>
		</div>
		<div class="b-board-header__images">
			<div class="b-board-header-images">
				<#if model.images?has_content && model.images.customLogoId?has_content && model.velocityBaseUrl?has_content>
					<div class="b-board-header-images__item">
						<img src="${model.velocityBaseUrl}/velocity/api/repository/v4/asset/${model.images.customLogoId}?token=${model.userToken}" class="b-logo-image">
					</div>
				</#if>
				<#if model.customLogoBase64?has_content>
					<div class="b-board-header-images__item">
						<img class="b-logo-image" src="data:image/png;base64,${model.customLogoBase64}">
					</div>
				</#if>
				<#if model.defaultImage?has_content>
					<div class="b-board-header-images__item">
						<div class="b-board-header-image">
							<div class="b-board-header-image__label">
								<div class="b-text b-text_description">Powered by</div>
							</div>
							<div class="b-board-header-image__icon">
								<img class="b-logo-image" src="data:image/png;base64,${model.defaultImage}" alt="">
							</div>
						</div>
					</div>
				</#if>
			</div>
		</div>
	</div>
</div>
</#macro>

<#macro renderReportSummary>
	<#if !VISIBILITY_OF_REPORT_SECTIONS.information>
		<#return>
	</#if>
	<@card headerTitle="">
		<@renderFormRow label=TEST_ASSET field=model.report.testName/>
		<@renderFormRow label=TEST_ASSET_LOCATION field=model.report.testPath/>
		<@renderFormRow label=RUNLIST_PATH field=model.report.runlistPath/>
		<@renderFormRow label=OWNER field=model.report.owner/>
		<#if model.report.detailLevel?has_content>
			<@renderFormRow label=REPORT_DETAIL_LEVEL field=getDetailLevelMessage()/>
		</#if>
		<#if model.report.startTime?has_content>
			<@renderFormRow label=EXECUTION_STARTED field=model.report.startTime?datetime/>
		</#if>
		<#if model.report.endTime?has_content>
			<@renderFormRow label=EXECUTION_ENDED field=model.report.endTime?datetime/>
		</#if>
		<@renderFormRow label=EXECUTION_DURATION field=model.report.duration/>
		<@renderFormRow label=EXECUTION_STATUS field=getStatusMessage()/>
		<@renderFormRow label=REPORT_ID field=model.report.reportId/>
		<@renderFormRow label=AGENT_HOST field=model.report.agentHost/>
		<@renderFormRow label=AGENT_NAME field=model.report.agentName/>
		<@renderFormRow label=PARAMETER_FILE_PATH field=model.report.parameterFilePath/>
		<@renderFormRow label=TOPOLOGY_NAME field=model.report.topologyName/>
		<@renderTopologyPreview/>
	</@card>
</#macro>

<#macro renderStatistics>
	<#if !VISIBILITY_OF_REPORT_SECTIONS.statistics>
		<#return>
	</#if>
	<@card headerTitle=STATISTICS_HEADER>
		<@renderFormRow label=TOTAL_REPORT_ITEMS field=model.report.totalItems/>
		<@renderFormRow label=TOTAL_ISSUES_COUNT field=model.report.totalIssues/>
		<@renderFormRow label=PASS_COUNT field=model.report.totalPass/>
		<@renderFormRow label=FAIL_COUNT field=model.report.totalFail/>
		<@renderFormRow label=ERROR_COUNT field=model.report.totalError/>
		<@renderFormRow label=WARNING_COUNT field=model.report.totalWarning/>
		<@renderFormRow label=INFORMATION_COUNT field=model.report.totalInfo/>
	</@card>
</#macro>

<#macro renderAgentRequirements>
	<#if !(model.report.requirements?has_content) || !VISIBILITY_OF_REPORT_SECTIONS.requirements>
		<#return/>
	</#if>
	<@card headerTitle=AGENT_REQUIREMENTS_HEADER>
		<#list model.report.requirements as requirement>
			<@renderFormRow label=requirement.name field=requirement.value/>
		</#list>
	</@card>
</#macro>

<#macro renderCharts>
	<#if !model.attachments?has_content>
		<#return>
	</#if>
	<@card headerTitle=CHARTS_HEADER>
		<#list model.attachments as chart>
			<#if chart?has_content && (chart.contentBase64?has_content || chart.pathToFile?has_content)>
				<#if chart.pathToFile?has_content>
				<a href="${chart.pathToFile}">
					<img class="b-test-case-chart" src="${chart.pathToFile}">
				</a>
				</#if>
				<#if chart.contentBase64?has_content>
				<a href="data:image/png;base64,${chart.contentBase64}">
					<img class="b-test-case-chart" src="data:image/png;base64,${chart.contentBase64}">
				</a>
				</#if>
			</#if>
		</#list>
	</@card>
</#macro>

<#macro renderTopologyPreview>
	<#assign isVelocityTopology=model.velocityBaseUrl?has_content && (model.report.topologyId?has_content || model.report.reservationId?has_content)>
	<#assign isItestTopology=model.report.topologyPathToFile?has_content>
	<#if !isVelocityTopology && !isItestTopology>
		<#return/>
	</#if>
<tr class="b-table-form-row">
	<th class="b-table-form__cell b-table-form__cell_label">
		<div class="b-table-form-cell b-table-form-cell_label">
			<div class="b-table-form-cell__label">
				<div class="b-label b-label_form">${TOPOLOGY}</div>
			</div>
		</div>
	</th>
	<td class="b-table-form__cell b-table-form__cell_field">
		<div class="b-table-form-field">
			<div class="b-table-form-field__cell">
				<div class="b-topology-preview">
					<#if isVelocityTopology>
						<div class="b-topology-preview__preview">
							<iframe class="b-topology-preview-iframe" scrolling="no"
									src="${getTopologyQuery(false)}"></iframe>
						</div>
						<div class="b-topology-preview__link">
							<a href="${getTopologyQuery(true)}" target="_parent" class="b-link b-link_full-size"></a>
						</div>
					</#if>
					<#if isItestTopology>
						<div class="b-topology-preview__preview">
							<a href="${model.report.topologyPathToFile}">
								<img class="b-topology-preview-image" src="${model.report.topologyPathToFile}" alt="">
							</a>
						</div>
					</#if>
				</div>
			</div>
		</div>
	</td>
</tr>
</#macro>

<#function getTopologyQuery isLink>
	<#assign topologyUrl = "${model.velocityBaseUrl}${isLink?then('/velocity/library/reservation-topology', '/webte/?embeddedMode=true')}">
	<#if model.report.topologyId?has_content>
		<#assign topologyUrl = topologyUrl + isLink?then("/${model.report.topologyId}", "&topologyId=${model.report.topologyId}")>
	</#if>
	<#if model.report.reservationId?has_content>
		<#return topologyUrl + isLink?then("?reservationId=${model.report.reservationId}", "&reservationId=${model.report.reservationId}")>
	</#if>
	<#return topologyUrl>
</#function>

<body>
<div class="b-board">
<@compress>
	<@renderReportHeader/>
	<@renderReportSummary/>
	<@renderStatistics/>
	<@renderCharts/>
	<@renderAgentRequirements/>
	<@renderParameters/>
	<@renderExtractedData/>
	<@renderExecutionIssues/>
</@compress>
    <@renderStepsTable/>
</div>
<script src="http://code.jquery.com/jquery-latest.js"></script>
<script>
	// Requires jQuery!
	jQuery.ajax({
		url: "https://jira.spirenteng.com/s/7c12bd15c3f501cbea98bd1cb8555b0b-T/-517za8/712002/5d6851480288ac036163ba466c120242/2.0.31/_/download/batch/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector-embededjs/com.atlassian.jira.collector.plugin.jira-issue-collector-plugin:issuecollector-embededjs.js?locale=en-US&collectorId=1f22bc99",
		type: "get",
		cache: true,
		dataType: "script"
	});

	summaryText = 'Nasty Bug';

	window.ATL_JQ_PAGE_PROPS = $.extend(window.ATL_JQ_PAGE_PROPS, {

		// ==== we add the code below to set the field values ====
		fieldValues: {
			description: createJiraIssueDesc(),
			summary: createJiraIssueSummary(),
			priority: '2'
		}
	});

	function createJiraIssueDesc() {
		var headerFields = ""

		// VERDIDT
		verdict = document.getElementsByClassName("b-test-case-result-label")[0].innerHTML;
		switch (verdict) {
			case "Passed":
				verdictColor = '1D8831';
				break;
			case "Failed":
				verdictColor = 'CE453C';
				break;
			case "Indeterminate":
				verdictColor = 'FED25D';
				break;
			default:
				verdictColor = 'FFFFFF';
		}
		headerFields = headerFields + '{panel:title=Verdict:|borderStyle=solid|borderColor=#ccc|titleBGColor=#F4F5F7|bgColor=#' + verdictColor + '}\n';
		headerFields = headerFields + verdict;
		headerFields = headerFields + '\n{panel}\n';

		// URL
		var velocityURL = "https://cw-vel.spirenteng.com"

		// PARSE THE HEADER TABLE
		var reportHdrTab = document.getElementById('reportHeader');
		// LOOP THROUGH EACH ROW OF THE HEADER TABLE
		for (i = 0; i < reportHdrTab.rows.length; i++) {

			// GET THE CELLS COLLECTION OF THE CURRENT ROW
			var objCells = reportHdrTab.rows.item(i).cells;
			// GET THE FIRST CELL
			var fc = objCells.item(0).innerText.replace(/\n/g, '')

			if (fc == "Automation Asset:" || fc == "Location:" || fc == "Report ID:") {
				headerFields = headerFields + '{panel:title=' + fc + '|borderStyle=solid|borderColor=#ccc|titleBGColor=#F4F5F7|bgColor=#FFFFFF}\n';
				switch (fc) {
					case "Report ID:":
						headerFields = headerFields + velocityURL + "/velocity/reports/executions/" + objCells.item(1).innerText.replace(/\n/g, '') + "/info";
						break;
					case "Automation Asset:":
						automationAsset = objCells.item(1).innerText.replace(/\n/g, '');
						headerFields = headerFields + objCells.item(1).innerText.replace(/\n/g, '');
						break;
					default:
						headerFields = headerFields + objCells.item(1).innerText.replace(/\n/g, '');
				}
				headerFields = headerFields + '\n{panel}\n';
			}
		}

		// PARSE THE EXECUTION MESSAGES TABLE
		var exeMsgTab = document.getElementById('executionMessages');
		executionMsgTable = "*Execution Messages*\n"
		executionMsgTable = executionMsgTable + "||{noformat}Step{noformat}||{noformat}Severity{noformat}||{noformat}Originator{noformat}||{noformat}Message{noformat}||";
		// LOOP THROUGH EACH ROW OF THE EXECUTION MESSAGES TABLE
		for (i = 0; i < exeMsgTab.rows.length; i++) {
			executionMsgTable = executionMsgTable + '\n|';

			// GET THE CELLS COLLECTION OF THE CURRENT ROW
			var objCells = exeMsgTab.rows.item(i).cells;

			// LOOP THROUGH EACH CELL OF THE CURRENT ROW TO READ CELL VALUES
			for (var j = 0; j < objCells.length; j++) {
				if (objCells.item(j).getElementsByClassName("b-icon").length == 1) {
					// THIS CELL INCLUDES A SEVERITY ICON
					switch (objCells.item(j).getElementsByClassName("b-icon")[0].className.split(" ")[1]) {
						case "b-icon_status-warning":
							executionMsgTable = executionMsgTable + '(!)|';
							break;
						case "b-icon_status-completed":
							executionMsgTable = executionMsgTable + '(/)|';
							break;
						case "b-icon_status-info":
							executionMsgTable = executionMsgTable + '(i)|';
							break;
						case "b-icon_status-failed":
							executionMsgTable = executionMsgTable + '(x)|';
							break;
					}
				}
				executionMsgTable = executionMsgTable + objCells.item(j).innerText.replace(/\n/g, '').replace(/\|/g, '\\|') + '|';
			}
		}
		return headerFields + executionMsgTable;
	}

	function createJiraIssueSummary() {
		return verdict + ": " + automationAsset;
	}
</script>
</body>
</html>
