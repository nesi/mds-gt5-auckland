<?xml version="1.0"?>

<!--                                                                 -->
<!-- APAC National Grid                                              -->
<!--                                                                 -->
<!-- XSL to transform XML output from National Facility software map -->
<!-- into APACGlueSoftwareSubset schema                                -->
<!--                                                                 -->
<!-- iVEC October 2006                                               -->
<!--                                                                 -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:glue="http://forge.cnaf.infn.it/glueschema/Spec/V12/R2" xmlns:apac="http://grid.apac.edu.au/glueschema/Spec/V12/R2">

<!-- Use html output to create complete emtpy elements -->
<!-- <xsl:output method="xml" indent="yes" omit-xml-declaration="yes"/> -->
<xsl:output method="xml" version="1.0" indent="yes"/>

<xsl:template match="softwaremap_xml_service/site/host">
  <xsl:element name="SoftwarePackages" namespace="http://www.ivec.org/softwareSubSchema/Spec/V12/R2">
    <xsl:for-each select="software/package">
      <apac:SoftwarePackage>
        <xsl:choose>
          <xsl:when test="starts-with(version/@name,'-')">
            <xsl:attribute name="LocalID"><xsl:value-of select="@name"/></xsl:attribute>
          </xsl:when>
          <xsl:otherwise>
            <xsl:attribute name="LocalID">
              <xsl:value-of select="@name"/>/<xsl:value-of select="version/@name"/>
            </xsl:attribute>
          </xsl:otherwise>
        </xsl:choose>
    
        <apac:Name><xsl:value-of select="@name"/></apac:Name>
    
        <xsl:if test="not(starts-with(version/@name,'-'))">
          <apac:Version><xsl:value-of select="version/@name"/></apac:Version>
        </xsl:if>

        <xsl:if test="string(version/module)">
          <apac:Module><xsl:value-of select="version/module"/></apac:Module>
        </xsl:if>

        <xsl:choose>
          <xsl:when test="contains('yes', version/serial/available)">
            <apac:SerialAvail>true</apac:SerialAvail>
          </xsl:when>
          <xsl:otherwise>
            <apac:SerialAvail>false</apac:SerialAvail>
          </xsl:otherwise>
        </xsl:choose>

        <xsl:choose>
          <xsl:when test="contains('yes', version/parallel/available)">
            <apac:ParallelAvail>true</apac:ParallelAvail>
          </xsl:when>
          <xsl:otherwise>
            <apac:ParallelAvail>false</apac:ParallelAvail>
          </xsl:otherwise>
        </xsl:choose>

        <apac:ParallelMaxCPUs><xsl:value-of select="version/parallel/max_cpus"/></apac:ParallelMaxCPUs>

        <xsl:for-each select="version/supported_parallel_types/parallel_type">
          <apac:SupportedParallelType><xsl:value-of select="node()"/></apac:SupportedParallelType>
        </xsl:for-each>

        <apac:LicenseType><xsl:value-of select="version/license_info"/></apac:LicenseType> 

        <xsl:if test="version/access_control_list/vo">
          <apac:ACL>
            <xsl:for-each select="version/access_control_list/vo">
              <glue:Rule><xsl:value-of select="node()"/></glue:Rule>
            </xsl:for-each>
          </apac:ACL>
        </xsl:if>

        <xsl:apply-templates select="version/executables"/>
        
      </apac:SoftwarePackage>
    </xsl:for-each>
  </xsl:element>
</xsl:template>

<xsl:template match="version/executables">
  <xsl:for-each select="executable">
    <apac:SoftwareExecutable>
      <xsl:attribute name="LocalID">
        <xsl:value-of select="@name"/>
      </xsl:attribute>
      <apac:Name><xsl:value-of select="@name"/></apac:Name>
     
      <apac:SerialAvail>true</apac:SerialAvail>

      <xsl:choose>
        <xsl:when test="contains('true', supports_parallel)">
          <apac:ParallelAvail>true</apac:ParallelAvail>
        </xsl:when>
        <xsl:otherwise>
          <apac:ParallelAvail>false</apac:ParallelAvail>
        </xsl:otherwise>
      </xsl:choose>
      <apac:ParallelMaxCPUs><xsl:value-of select="max_cpus"/></apac:ParallelMaxCPUs>

      <apac:ParallelType><xsl:value-of select="supported_parallel_type"/></apac:ParallelType>

    </apac:SoftwareExecutable>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet>
