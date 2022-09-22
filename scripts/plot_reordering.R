args = commandArgs(trailingOnly=TRUE)

bn<-read.table(args[1], sep=" ", header=F)
wrr<-read.table(args[2], sep=" ", header=F)

pdf(args[3])
min1 <- min(bn$V2)
min2 <- min(wrr$V2)
max1 <- max(bn$V2)
max2 <- max(wrr$V2)
plot(bn$V1, bn$V2, xlab="Number of paths, M", ylab="Average reordering distance", type="b", col="dark blue", pch=2, lwd=3, ylim=c(min(c(min1, min2)), max(c(max1, max2))))
segments(bn$V1, bn$V2-bn$V3, bn$V1, bn$V2+bn$V3, col="dark blue", lwd=1)
epsilon = 0.02
segments(bn$V1-epsilon, bn$V2-bn$V3, bn$V1+epsilon, bn$V2-bn$V3, col="dark blue", lwd=1)
segments(bn$V1-epsilon, bn$V2+bn$V3, bn$V1+epsilon, bn$V2+bn$V3, col="dark blue", lwd=1)
points(wrr$V1, wrr$V2, type="b", col="dark red", pch=5, lwd=3)
segments(wrr$V1, wrr$V2-wrr$V3, wrr$V1, wrr$V2+wrr$V3, col="dark red", lwd=1)
epsilon = 0.02
segments(wrr$V1-epsilon, wrr$V2-wrr$V3, wrr$V1+epsilon, wrr$V2-wrr$V3, col="dark red", lwd=1)
segments(wrr$V1-epsilon, wrr$V2+wrr$V3, wrr$V1+epsilon, wrr$V2+wrr$V3, col="dark red", lwd=1)
grid(lwd=2)
legend("bottomright", c("BN", "WRR"), pch=c(2,5), lty=c(1,1), inset=c(0,1), xpd=TRUE, horiz=TRUE, bty="n", col=c("dark blue", "dark red"), lwd=3)
dev.off()
