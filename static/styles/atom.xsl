<?xml version="1.0" encoding="utf-8"?>
	<xsl:stylesheet version="3.0"
	                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	                xmlns:atom="http://www.w3.org/2005/Atom">
	  <xsl:output method="html" encoding="UTF-8" indent="yes" />
	  <xsl:template match="/">
	    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
	      <head>
	        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
	        <title>Feed | <xsl:value-of select="atom:feed/atom:title" /></title>
	        <link rel="stylesheet" href="/styles/atom.css" />
	        <link rel="icon shortcut" href="/images/logos/exeami.webp"/>
	      </head>
	      <body>
	        <div class="content">
	        <div class="container h-feed">
	          <section>
	            <p class="center-text">This is an Atom feed. Visit 
	            <a href="https://aboutfeeds.com">About Feeds</a> to
            learn more and get started. It’s free.
	           </p>
	            <p class="center-text">
	              This is a <strong>feed preview</strong> without complete content, use a feed reader to see everything.
	            </p>
	            <h1>
	              <xsl:value-of select="atom:feed/atom:title" />
	            </h1>
	            <ul class="feed-list e-content">
	              <xsl:for-each select="atom:feed/atom:entry">
	                <li class="h-entry list-item-wrap">
	                  <h2 class="p-name entry-title">
	                    <a class="u-url u-syndication">
	                      <xsl:attribute name="href">
	                        <xsl:value-of select="atom:link/@href" />
	                      </xsl:attribute>
	                      <xsl:value-of select="atom:title" />
	                    </a>
	                    <time class="dt-published">
	                      <xsl:attribute name="datetime">
	                        <xsl:value-of select="atom:updated" />
	                      </xsl:attribute>
	                      <xsl:value-of select="substring(atom:updated, 0, 11)" />
	                    </time>
	                  </h2>
	                  <p class="p-summary">
	                    <xsl:value-of select="atom:summary" />
	                  </p>
	                </li>
	              </xsl:for-each>
	            </ul>
	          </section>
	        </div>
	        </div>
	      </body>
	    </html>
	  </xsl:template>
	</xsl:stylesheet>
