profiles <- read.csv("profiles.csv", check.names=FALSE)
base <- subset(read.csv("sensitivity.csv"), case == "dz-0.005")
png("isolated-wells.png", width=1800, height=1050, res=180, type="cairo")
par(mar=c(4.6, 4.7, 3.0, 1.2), las=1, family="sans", mgp=c(2.65, 0.7, 0))
plot(NA, xlim=c(-20,47), ylim=c(-60,177), xlab="Position z (nm)", ylab="Energy (meV)",
     xaxs="i", yaxs="i", bty="l", xaxt="n", yaxt="n")
axis(1, at=seq(-20,45,5), col="#607082", col.axis="#24354a")
axis(2, at=seq(-60,160,20), col="#607082", col.axis="#24354a")
abline(h=seq(-60,160,20), col="#e4e9ed", lwd=0.75)
rect(33.41, -60, 38.41, 177, col="#f3eddd", border=NA)
interfaces <- c(-20,-16,0,4.3,13.2,15.66,23.81,27.91,43.91,47)
barriers <- rep(c(TRUE,FALSE), length.out=length(interfaces)-1)
for (i in seq_along(barriers)) {
    endpoints <- interfaces[i + c(0,1)]
    upper <- if (barriers[i]) 149 else 0
    lines(endpoints, upper-1.22*endpoints, col="#20374a", lwd=2)
    if (i < length(barriers)) {
        segments(endpoints[2], -1.22*endpoints[2], endpoints[2], 149-1.22*endpoints[2],
                 col="#20374a", lwd=2)
    }
}
labels <- c("g", "l", "u", "e", "g′")
levels <- c(base$g, base$l, base$u, base$e, base$g_next)
colors <- c("#254879", "#296547", "#168258", "#9e3c31", "#a86220")
bounds <- list(c(-20,3), c(1,28), c(1,28), c(24,46), c(24,46))
label_x <- c(-17, 1.5, 20, 26.5, 42.5)
for (i in seq_along(labels)) {
    visible <- profiles$z_nm >= bounds[[i]][1] & profiles$z_nm <= bounds[[i]][2]
    x <- profiles$z_nm[visible]
    y <- levels[i] + 200 * profiles[visible,i+2]
    segments(min(x), levels[i], max(x), levels[i], col=colors[i], lty=3, lwd=0.8)
    lines(x, y, col=colors[i], lwd=2)
    text(label_x[i], levels[i]+4, labels[i], col=colors[i], font=2, cex=0.95)
}
text(c(-8,14,36), c(66,153,45), c("Upstream phonon well", "Lasing double well", "Downstream phonon well"),
     col="#24354a", cex=0.77)
text(35.91, 159, "Si-doped", cex=0.76, col="#74562c")
mtext("12.2 kV/cm  •  149 meV offset  •  all state densities share one vertical scale",
      side=3, line=1, adj=0, cex=0.82, col="#24354a")
dev.off()
