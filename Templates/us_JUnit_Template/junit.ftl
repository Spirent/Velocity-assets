<#ftl output_format="XML">
<#assign 
failedSteps = []
failureMessages = {}
numTests = 0
numFailures = 0
/>
<#macro doNotRemove>
</#macro>
<testsuites>
<#list model.issues as issue>
  <#if issue.originator = "exec.run">
    <#assign numTests += 1>
    <#if issue.severity = "ERROR">
      <#assign failedSteps = failedSteps + [ issue.stepId ]/>
      <#assign numFailures += 1/>
      <#assign failureMessages = failureMessages + { issue.stepId : issue.message }/>
    </#if>
  </#if>
</#list>
<testsuite name="${model.report.testName?remove_ending(".fftc")}" errors="${model.report.totalFail}" tests="${numTests}" failures="${numFailures}" time="${model.report.duration}" timestamp="${model.report.endTime?datetime}">
<#list model.steps as step>
  <#if step.action = "run">
    <testcase assertions="1" name="${step.command}" time="${step.startOffset}" classname="${model.report.testName?remove_ending(".fftc")}.suite">
    <#if step.response?has_content>
	  <#assign lines=step.response?split("(\r\n|\r|\n)|$", 'r')>
      <system-out>
        <![CDATA[
        <#list lines as responseLine>
          ${responseLine}
        </#list>
        ]]>
    </system-out>
    </#if>
    <#if failedSteps?seq_contains(step.stepId)>
        <failure type="itest" message="${failureMessages[step.stepId]}"></failure>
    </#if>
    </testcase>
  </#if>
</#list>
</testsuite>
</testsuites>
