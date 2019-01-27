<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
 xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions"
 xmlns:func="http://service.wsgc.com/2014/xsltcustomfunction"  xmlns:cle= "http://www.wsgc.com/schemas/common/CLEFlags.xsd" >
	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
	<xsl:param name="paramdoc"/>
	<xsl:function name="func:MaskStr">
		<xsl:param name="str"/> 
		<xsl:param name="fc"/> 
		<xsl:param name="lc"/> 
		<xsl:param name="chr"/> 
		<xsl:variable name="mlen" select="xs:integer(fn:string-length($str) - xs:integer($fc) -xs:integer($lc))"/>
		<xsl:variable name="pad">
			<xsl:choose>
				<xsl:when test="$mlen > 0">
					<xsl:for-each select="1 to $mlen">
						<xsl:value-of select="$chr" />
					</xsl:for-each>
				</xsl:when>
			</xsl:choose>
		</xsl:variable>
		<xsl:value-of select="fn:concat(fn:substring($str,1,xs:integer($fc)),$pad,fn:substring($str,fn:string-length($str)-xs:integer($lc) + 1,xs:integer($lc)))"/>

	</xsl:function>

	<xsl:template match="/">
		<xsl:copy>
			<xsl:apply-templates select="node()"/>
		</xsl:copy>
	</xsl:template>


	<xsl:template match="*">
		<xsl:variable name="lname"  select="local-name()"/>
		<xsl:variable name="plname"  select="../local-name()"/>
		<xsl:choose>
			<xsl:when  test="$paramdoc/cle:Masks/cle:Mask[ ./cle:TargetParentElement=$plname and  ./cle:TargetElement=$lname ]">
				<xsl:element name="{name()}" namespace="{namespace-uri()}">
					<xsl:variable name="cparamdoc" select="$paramdoc/cle:Masks/cle:Mask[./cle:TargetParentElement=$plname and  ./cle:TargetElement=$lname ]"/>
					<xsl:value-of select="func:MaskStr(.,$cparamdoc/cle:NumOfFirstCharToRetain,$cparamdoc/cle:NumOfLastCharToRetain,$cparamdoc/cle:MaskChar)"/>
					
				</xsl:element>
				<xsl:apply-templates select="@*"/>
				<xsl:apply-templates select="*"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:element name="{name()}" namespace="{namespace-uri()}">
					<xsl:apply-templates select="@*"/>
					<xsl:apply-templates/>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<xsl:template match="@*">
		<xsl:variable name="alname"  select="local-name()"/>
		<xsl:variable name="aplname"  select="../local-name()"/>
		<xsl:attribute name="{name()}" namespace="{namespace-uri()}">
		<xsl:choose>
				<xsl:when  test="$paramdoc/cle:Masks/cle:Mask[ ./cle:TargetParentElement=$aplname and  ./cle:TargetElement=$alname ]">
				   <xsl:variable name="cparamdoc" select="$paramdoc/cle:Masks/cle:Mask[ ./cle:TargetParentElement=$aplname and  ./cle:TargetElement=$alname ]"/>
					<xsl:value-of select="func:MaskStr(.,$cparamdoc/cle:NumOfFirstCharToRetain,$cparamdoc/cle:NumOfLastCharToRetain,$cparamdoc/cle:MaskChar)"/>
 
					
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="."/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:attribute>
	</xsl:template>
	
	<xsl:template match="text()">
		<xsl:copy/>
	</xsl:template>
</xsl:stylesheet>